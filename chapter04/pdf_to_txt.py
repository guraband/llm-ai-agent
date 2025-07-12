import pymupdf
import os

pdf_file_path = "./chapter04/doc/과정기반 작물모형을 이용한 웹 기반 밀 재배관리 의사결정 지원시스템 설계 및 구축.pdf"
doc = pymupdf.open(pdf_file_path)

full_txt = ''

for page in doc:
    text = page.get_text()
    full_txt += text

pdf_file_name = os.path.basename(pdf_file_path)
pdf_file_name = os.path.splitext(pdf_file_name)[0]  # 확장자 제거

txt_file_path = f"./chapter04/output/{pdf_file_name}.txt"
with open(txt_file_path, 'w', encoding='utf-8') as f:
    f.write(full_txt)

print(f"파일 저장 완료: {txt_file_path}")
