# app.py

import streamlit as st

# 认证
from openai import OpenAI



# 预定义三种样式模板
templates = {
    "国企": "请根据以下关键词生成我的工作日报：“{}”\n\n，要求行文风格使用中国国企的严谨风格",
    "互联网": "请根据以下关键词生成我的工作日报：“{}”\n\n，要求行文风格使用互联网企业的汇报风格",
    "浮夸": "请根据以下关键词生成我的工作日报：“{}”\n\n，要求行文风格使用浮夸的词汇的汇报风格",
    "简洁": "请根据以下关键词生成我的工作日报：“{}”\n\n，要求行文风格使用简单风格",
}

# 根据选择的样式返回相应的模板
def get_template(style):
    return templates[style]


# 使用 GPT-3 生成日报内容
def generate_report(api_key, keywords, template):
    prompt = f"{template.format(keywords)}"
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    report = response.choices[0].message.content.strip()
    return report


# 生成界面
def main():
    st.title("工作日报生成器")
    api_key = st.text_input("请输入您的API Key：")
    # 获取用户输入的关键词
    keywords = st.text_input("请输入您今天完成的工作（每条工作请以回车隔开）：")
    keywords = keywords.strip().replace("\n", "\n- ")

    # 获取用户选择的样式
    style = st.selectbox("请选择日报样式：", options=["国企", "浮夸", "互联网", "简洁"])

    # 生成日报内容
    template = get_template(style)
    report = generate_report(api_key, keywords, template)

    # 显示生成的日报内容
    st.write("以下是您的工作日报：")
    st.write(report)


if __name__ == "__main__":
    main()
