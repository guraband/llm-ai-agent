import os
import pymupdf
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime


def extract_text_without_header_footer(pdf_file_path, header_height=80, footer_height=80):
    doc = pymupdf.open(pdf_file_path)
    full_txt = ''
    for page in doc:
        rect = page.rect
        text = page.get_text(
            clip=(0, header_height, rect.width, rect.height-footer_height))
        full_txt += text + '\n---------------------------\n'
    pdf_file_name = os.path.basename(pdf_file_path)
    pdf_file_name = os.path.splitext(pdf_file_name)[0]  # 확장자 제거
    txt_file_path = f"./chapter04/output/{
        pdf_file_name}_with_preprocessing.txt"
    with open(txt_file_path, 'w', encoding='utf-8') as f:
        f.write(full_txt)
    print(f"본문 텍스트 파일 저장 완료: {txt_file_path}")
    return txt_file_path


def summarize_text(file_path: str, client):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    system_prompt = f"""
        너는 다음 글을 요약하는 봇이다. 아래 글을 읽고, 저자의 문제 인식과 주장을 파악하고, 주요 내용을 요약하라.
        작성해야 하는 포맷은 다음과 같다.

        # 제목

        ## 저자의 문제 인식 및 주장 (15문장 이내. 문장과 문장 사이에는 줄바꿈 적용)

        ## 저자 소개

        =============== 이하 텍스트 ===============
        {text}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        messages=[
            {"role": "system", "content": system_prompt},
        ]
    )
    return response.choices[0].message.content


def main():
    load_dotenv()
    api_key = os.getenv("STUDY_OPENAI_API_KEY")
    if not api_key:
        raise ValueError("STUDY_OPENAI_API_KEY 환경변수가 설정되어 있지 않습니다.")
    client = OpenAI(api_key=api_key)

    pdf_file_path = input("PDF 파일 경로를 입력하세요: ").strip()
    if not os.path.exists(pdf_file_path):
        print(f"파일이 존재하지 않습니다: {pdf_file_path}")
        return

    # 1. PDF 전처리 및 txt 저장
    txt_file_path = extract_text_without_header_footer(pdf_file_path)

    # 2. 요약 및 summary 파일 저장
    summary = summarize_text(txt_file_path, client)
    output_dir = "./chapter04/output"
    # 순번 결정
    idx = 1
    while True:
        summary_file_path = os.path.join(
            output_dir, f"summary_{idx}.txt")
        if not os.path.exists(summary_file_path):
            break
        idx += 1
    with open(summary_file_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"요약 파일 저장 완료: {summary_file_path}")


if __name__ == "__main__":
    main()
