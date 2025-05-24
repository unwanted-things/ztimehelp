import datetime
import requests
from typing import Dict, List, Optional, Union
import jwt

from ztimehelp.data.utils import get_date_object


class ZoomStats:
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        date: datetime,
        user_id: Optional[str] = "me",
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.user_id = "me"
        self.base_url = "https://api.zoom.us/v2"

        dateobj = get_date_object(date,False)

        self.start_date = self._format_date(dateobj["start_date"])
        self.end_date = self._format_date(dateobj["end_date"])

        if not user_id:
            raise ValueError("Either user_email or user_id must be provided")

    def _format_date(self, date: datetime.datetime) -> str:
        return date.strftime("%Y-%m-%d")

    def _generate_jwt_token(self) -> str:
        token_exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            minutes=30
        )
        payload = {"iss": self.api_key, "exp": token_exp.timestamp()}
        token = jwt.encode(payload, self.api_secret, algorithm="HS256")

        if isinstance(token, bytes):
            return token.decode("utf-8")
        return token

    def _make_request(
        self, endpoint: str, params: Optional[Dict] = None, method: str = "GET"
    ) -> Union[List, Dict]:
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self._generate_jwt_token()}",
            "Content-Type": "application/json",
        }

        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        else:
            response = requests.post(url, headers=headers, json=params)

        response.raise_for_status()
        return response.json()

    def get_user_meetings(self) -> Dict:
        endpoint = f"/past_meetings/{self.user_id}/instances"
        params = {
            "from": self.start_date,
            "to": self.end_date,
            "page_size": 100,
            "timezone": "Asia/Kolkata",
        }

        print(params)

        past_meetings = self._make_request(endpoint, params)

        return self._get_meetings_with_duration(past_meetings)

    def _get_meetings_with_duration(self, meetings: List[Dict]) -> Dict:
        meetings_with_duration = []
        total_duration = 0

        for meeting in meetings:
            meeting_id = meeting.get("id")

            endpoint = f"/past_meetings/{meeting_id}/participants"
            participants_data = self._make_request(endpoint)
            participants = participants_data.get("participants", [])

            user_sessions = []
            for participant in participants:
                if (
                    participant.get("email") == self.user_email
                    or participant.get("user_id") == self.user_id
                ):
                    join_time = participant.get("join_time")
                    leave_time = participant.get("leave_time")

                    if join_time and leave_time:
                        join_dt = datetime.datetime.fromisoformat(
                            join_time.replace("Z", "+00:00")
                        )
                        leave_dt = datetime.datetime.fromisoformat(
                            leave_time.replace("Z", "+00:00")
                        )
                        duration_minutes = int(
                            (leave_dt - join_dt).total_seconds() / 60
                        )

                        user_sessions.append(
                            {
                                "join_time": join_time,
                                "leave_time": leave_time,
                                "duration_minutes": duration_minutes,
                            }
                        )

            if user_sessions:
                meeting_duration = sum(
                    session["duration_minutes"] for session in user_sessions
                )
                total_duration += meeting_duration

                meetings_with_duration.append(
                    {
                        "id": meeting_id,
                        "topic": meeting.get("topic", "Untitled Meeting"),
                        "start_time": meeting.get("start_time"),
                        "duration_minutes": meeting_duration,
                        "sessions": user_sessions,
                    }
                )

        return {
            "meetings": meetings_with_duration,
            "total_count": len(meetings_with_duration),
            "total_duration_minutes": total_duration,
        }

    def get_daily_meetings_summary(self) -> Dict:
        meetings_data = self.get_user_meetings()

        return {
            "total_meetings": meetings_data["total_count"],
            "total_duration_minutes": meetings_data["total_duration_minutes"],
            "meetings": meetings_data["meetings"],
        }
