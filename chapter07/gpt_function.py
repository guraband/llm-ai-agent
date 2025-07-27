from datetime import datetime
import pytz


def get_current_time(timezone: str = "Asia/Seoul"):
    print("timezone : ", timezone)
    tz = pytz.timezone(timezone)
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    now_timezone = f'{now} {timezone}'
    print(now_timezone)
    return now_timezone


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "해당 타임존의 현재 날짜와 시간을 반환합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "현재 날짜와 시간을 반환할 타임존 이름 (예: Asia/Seoul)"}
                },
                "required": ["timezone"]
            }
        }
    }
]

if __name__ == "__main__":
    print(get_current_time())
