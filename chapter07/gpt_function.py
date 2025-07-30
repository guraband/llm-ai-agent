from datetime import datetime
from typing import Dict, Any, List, Optional
import pytz
import yfinance as yf
import json
import logging

# 상수 정의
DEFAULT_TIMEZONE = "Asia/Seoul"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
STOCK_INFO_KEYS = [
    "longName", "currentPrice", "marketCap", "volume",
    "previousClose", "open", "dayLow", "dayHigh",
    "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "currency"
]

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_current_time(timezone: str = DEFAULT_TIMEZONE) -> str:
    """
    지정된 타임존의 현재 날짜와 시간을 반환합니다.

    Args:
        timezone (str): 타임존 이름 (예: Asia/Seoul, US/Eastern)

    Returns:
        str: 형식화된 현재 날짜와 시간 문자열

    Raises:
        ValueError: 유효하지 않은 타임존일 경우
    """
    try:
        logger.info(f"타임존 요청: {timezone}")

        # 타임존 유효성 검사
        if timezone not in pytz.all_timezones_set:
            available_timezones = [
                "Asia/Seoul", "US/Eastern", "US/Pacific", "Europe/London", "UTC"]
            raise ValueError(
                f"유효하지 않은 타임존: {timezone}. "
                f"사용 가능한 타임존 예시: {', '.join(available_timezones)}"
            )

        tz = pytz.timezone(timezone)
        now = datetime.now(tz).strftime(TIME_FORMAT)
        result = f'{now} {timezone}'

        logger.info(f"현재 시간: {result}")
        return result

    except Exception as e:
        error_msg = f"시간 조회 중 오류 발생: {str(e)}"
        logger.error(error_msg)
        return error_msg


def get_yf_stock_info(ticker: str) -> str:
    """
    Yahoo Finance에서 지정된 종목의 주식 정보를 조회합니다.

    Args:
        ticker (str): 종목 코드 (예: AAPL, GOOGL, SCHD)

    Returns:
        str: JSON 형태의 주식 정보 문자열

    Raises:
        ValueError: 유효하지 않은 종목 코드일 경우
    """
    try:
        logger.info(f"주식 정보 조회: {ticker}")

        # 입력값 검증
        if not ticker or not isinstance(ticker, str):
            raise ValueError("유효한 종목 코드를 입력해주세요.")

        ticker_obj = yf.Ticker(ticker.upper())
        info = ticker_obj.info

        # 데이터 유효성 검사
        if not info or 'symbol' not in info:
            raise ValueError(f"종목 '{ticker}'에 대한 정보를 찾을 수 없습니다.")

        # 필요한 정보만 추출하여 구조화
        filtered_info = extract_key_stock_info(info)
        result = json.dumps(filtered_info, ensure_ascii=False, indent=2)

        logger.info(f"주식 정보 조회 완료: {ticker}")
        return result

    except Exception as e:
        error_msg = f"주식 정보 조회 중 오류 발생 (종목: {ticker}): {str(e)}"
        logger.error(error_msg)
        return json.dumps({"error": error_msg}, ensure_ascii=False)


def get_yf_stock_history(ticker: str, period: str = "1d") -> str:
    """
    Yahoo Finance에서 지정된 종목의 주식 히스토리 데이터를 조회합니다.

    Args:
        ticker (str): 종목 코드 (예: AAPL, GOOGL, SCHD)
        period (str): 조회 기간 (예: 1d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)

    Returns:
        str: 마크다운 형태의 주식 히스토리 데이터 문자열

    Raises:
        ValueError: 유효하지 않은 종목 코드나 기간일 경우
    """
    try:
        logger.info(f"주식 히스토리 조회: {ticker}, 기간: {period}")

        # 입력값 검증
        if not ticker or not isinstance(ticker, str):
            raise ValueError("유효한 종목 코드를 입력해주세요.")

        valid_periods = ["1d", "5d", "1mo", "3mo",
                         "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
        if period not in valid_periods:
            valid_str = ", ".join(valid_periods)
            raise ValueError(f"유효하지 않은 기간: {period}. 사용 가능한 기간: {valid_str}")

        ticker_obj = yf.Ticker(ticker.upper())
        history = ticker_obj.history(period=period)

        # 데이터 유효성 검사
        if history.empty:
            raise ValueError(f"종목 '{ticker}'에 대한 히스토리 데이터를 찾을 수 없습니다.")

        # 데이터를 마크다운 형태로 변환
        history_md = history.to_markdown()

        logger.info(f"주식 히스토리 조회 완료: {ticker}")
        return history_md

    except Exception as e:
        error_msg = f"주식 히스토리 조회 중 오류 발생 (종목: {ticker}, 기간: {
            period}): {str(e)}"
        logger.error(error_msg)
        return f"ERROR: {error_msg}"


def get_yf_stock_recommendations(ticker: str) -> str:
    """
    Yahoo Finance에서 지정된 종목의 주식 추천 정보를 조회합니다.

    Args:
        ticker (str): 종목 코드 (예: AAPL, GOOGL, SCHD)

    Returns:
        str: 마크다운 형태의 주식 추천 정보 문자열

    Raises:
        ValueError: 유효하지 않은 종목 코드일 경우
    """
    try:
        logger.info(f"주식 추천 정보 조회: {ticker}")

        # 입력값 검증
        if not ticker or not isinstance(ticker, str):
            raise ValueError("유효한 종목 코드를 입력해주세요.")

        ticker_obj = yf.Ticker(ticker.upper())
        recommendations = ticker_obj.recommendations

        # 데이터 유효성 검사
        if recommendations is None or recommendations.empty:
            raise ValueError(f"종목 '{ticker}'에 대한 추천 정보를 찾을 수 없습니다.")

        # 데이터를 마크다운 형태로 변환
        recommendations_md = recommendations.to_markdown()

        logger.info(f"주식 추천 정보 조회 완료: {ticker}")
        return recommendations_md

    except Exception as e:
        error_msg = f"주식 추천 정보 조회 중 오류 발생 (종목: {ticker}): {str(e)}"
        logger.error(error_msg)
        return f"ERROR: {error_msg}"


def extract_key_stock_info(info: Dict[str, Any]) -> Dict[str, Any]:
    """
    주식 정보에서 핵심 데이터만 추출합니다.

    Args:
        info (Dict[str, Any]): Yahoo Finance에서 받은 전체 주식 정보

    Returns:
        Dict[str, Any]: 핵심 주식 정보만 포함된 딕셔너리
    """
    filtered_info = {}

    for key in STOCK_INFO_KEYS:
        if key in info:
            filtered_info[key] = info[key]

    # 추가 계산된 정보
    if 'currentPrice' in filtered_info and 'previousClose' in filtered_info:
        current = filtered_info['currentPrice']
        previous = filtered_info['previousClose']
        if current and previous:
            change = current - previous
            change_percent = (change / previous) * 100
            filtered_info['priceChange'] = round(change, 2)
            filtered_info['priceChangePercent'] = round(change_percent, 2)

    return filtered_info


def get_available_timezones() -> List[str]:
    """
    자주 사용되는 타임존 목록을 반환합니다.

    Returns:
        List[str]: 타임존 이름 리스트
    """
    common_timezones = [
        "Asia/Seoul", "Asia/Tokyo", "Asia/Shanghai",
        "US/Eastern", "US/Central", "US/Mountain", "US/Pacific",
        "Europe/London", "Europe/Paris", "Europe/Berlin",
        "UTC", "GMT"
    ]
    return common_timezones


def create_function_tool(name: str, description: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    OpenAI Function calling 형식의 tool 객체를 생성합니다.

    Args:
        name (str): 함수 이름
        description (str): 함수 설명
        parameters (Dict[str, Any]): 함수 매개변수 스키마

    Returns:
        Dict[str, Any]: OpenAI Function calling 형식의 tool 객체
    """
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": parameters
        }
    }


# Tools 정의를 함수로 생성하여 유지보수성 향상
def get_tools() -> List[Dict[str, Any]]:
    """
    사용 가능한 모든 function tools를 반환합니다.

    Returns:
        List[Dict[str, Any]]: OpenAI Function calling 형식의 tools 리스트
    """
    timezone_tool = create_function_tool(
        name="get_current_time",
        description="지정된 타임존의 현재 날짜와 시간을 반환합니다. 타임존이 지정되지 않으면 한국 시간(Asia/Seoul)을 기본값으로 사용합니다.",
        parameters={
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": f"현재 날짜와 시간을 반환할 타임존 이름. 예시: {', '.join(get_available_timezones()[:5])}",
                    "default": DEFAULT_TIMEZONE
                }
            },
            "required": ["timezone"]
        }
    )

    stock_tool = create_function_tool(
        name="get_yf_stock_info",
        description="Yahoo Finance에서 지정된 종목의 주식 정보를 조회합니다. 현재가, 전일 대비, 거래량, 시가총액 등의 정보를 제공합니다.",
        parameters={
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "조회할 종목의 티커 심볼. 예시: AAPL (애플), GOOGL (구글), MSFT (마이크로소프트), SCHD (ETF)"
                }
            },
            "required": ["ticker"]
        }
    )

    stock_history_tool = create_function_tool(
        name="get_yf_stock_history",
        description="Yahoo Finance에서 지정된 종목의 주식 일봉 데이터를 조회합니다.",
        parameters={
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "조회할 종목의 티커 심볼. 예시: AAPL (애플), GOOGL (구글), MSFT (마이크로소프트), SCHD (ETF)"
                },
                "period": {
                    "type": "string",
                    "description": "조회할 기간. 예시: 1d (1일), 1mo (1개월), 3mo (3개월), 6mo (6개월), 1y (1년), 2y (2년), 5y (5년), 10y (10년), ytd (올해 주식 시작 이후), max (최대 기간)",
                    "default": "1d"
                }
            },
            "required": ["ticker", "period"]
        }
    )

    stock_recommendations_tool = create_function_tool(
        name="get_yf_stock_recommendations",
        description="Yahoo Finance에서 지정된 종목의 주식 추천 정보를 조회합니다.",
        parameters={
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "조회할 종목의 티커 심볼. 예시: AAPL (애플), GOOGL (구글), MSFT (마이크로소프트), SCHD (ETF)"
                }
            },
            "required": ["ticker"]
        }
    )

    return [timezone_tool, stock_tool, stock_history_tool, stock_recommendations_tool]


# 하위 호환성을 위해 기존 tools 변수 유지
tools = get_tools()


def main() -> None:
    """
    메인 함수: 모든 함수들을 테스트합니다.
    """
    print("=== GPT Function Tools 테스트 ===\n")

    # Tools 정보
    print("# 등록된 Tools 개수:", len(tools))

    # 시간 조회 테스트
    print("1. 현재 시간 조회 테스트:")
    print(f"한국 시간: {get_current_time()}")
    print(f"미국 동부 시간: {get_current_time('US/Eastern')}")
    print()

    # 주식 정보 조회 테스트
    print("2. 주식 정보 조회 테스트:")
    print(f"SCHD 정보:\n{get_yf_stock_info('SCHD')}")
    print()

    # 사용 가능한 타임존 목록
    print("3. 사용 가능한 타임존:")
    print(", ".join(get_available_timezones()))
    print()

    # 주식 일봉 데이터 조회 테스트
    print("4. 주식 일봉 데이터 조회 테스트:")
    print(f"SCHD 일봉 데이터:\n{get_yf_stock_history('SCHD')}")
    print()

    # 주식 추천 정보 조회 테스트
    print("5. 주식 추천 정보 조회 테스트:")
    print(f"TSLA 추천 정보:\n{get_yf_stock_recommendations('TSLA')}")


if __name__ == "__main__":
    main()
