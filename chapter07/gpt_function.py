from datetime import datetime
import pytz
import yfinance as yf


def get_current_time(timezone: str = "Asia/Seoul"):
    print("timezone : ", timezone)
    tz = pytz.timezone(timezone)
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    now_timezone = f'{now} {timezone}'
    print(now_timezone)
    return now_timezone


def get_yf_stock_info(ticker: str):
    ticker = yf.Ticker(ticker)
    info = ticker.info
    print(info)
    return str(info)


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
    },
    {
        "type": "function",
        "function": {
            "name": "get_yf_stock_info",
            "description": "해당 종목의 Yahoo Finance 주식 정보를 반환합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "종목 코드 (예: SCHD)"}
                },
                "required": ["ticker"]
            }
        }
    }
]

if __name__ == "__main__":
    print(get_current_time())
    print(get_yf_stock_info("SCHD"))
