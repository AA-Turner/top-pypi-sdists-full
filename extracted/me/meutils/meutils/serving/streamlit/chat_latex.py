#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatbot
# @Time         : 2023/10/27 14:31
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://nicedouble-streamlitantdcomponentsdemo-app-middmy.streamlit.app/
from langchain.prompts import ChatPromptTemplate

from chatllm.llmchain.decorators import llm_stream
from meutils.pipe import *
from meutils.ai_cv.latex_ocr import latex_ocr
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

import streamlit as st
from streamlit_extras.streaming_write import write




class ChatMessage(BaseModel):
    name: str = "assistant"  # "user", "assistant", or str
    avatar: Optional[str] = None
    generator: Any = '我是一条内容'


def chat_message(message: ChatMessage, help: Optional[str] = None, message_hook: Optional[Callable] = None):
    """
        chat_message(ChatMessage())
        chat_message(ChatMessage(name='assistant'))

        def chat_messages(messages: List[ChatMessage]):
            for msg in messages:
                chat_message(msg)

        chat_messages([ChatMessage()] * 10)
    """
    with st.chat_message(name=message.name, avatar=message.avatar):
        # message_placeholder = st.empty()
        # response = ''
        # for token in message.generator:
        #     # Display robot response in chat message container
        #     # time.sleep(0.1)
        #     # token = repr(f"""{token}""").strip("'")
        #     response += token
        #     message_placeholder.markdown(response + "▌")
        #
        # message_placeholder.markdown(response, unsafe_allow_html=True, help=help)

        # def fn():
        #     yield from message.generator

        write(message.generator)

        if message_hook: message_hook()


def ai_reply(user_input):
    template = ChatPromptTemplate.from_messages([
        ("system",
         """
         你是一名数学专家，你的名字叫火宝🔥
         要求：
         1. Let's think step by step. 
         2. 如果答案遇到公式请用标准的latex输出，公式用$包裹，例如：$\sqrt{{x^2+y^2}}=1$
         3. 务必用中文回答
         """.strip()),
        ('human', '开始解题：\n```{user_input}```')
    ])

    llm = LLMChain(llm=ChatOpenAI(model_name="gpt-4-0613", temperature=0, streaming=True), prompt=template)
    output = llm_stream(llm.run)(user_input=user_input)  # "gpt-3.5-"
    return output


if __name__ == '__main__':
    st.markdown('### 🔥解题小能手')

    # st.markdown(r':green[$\text{求极限}\lim_{x\to0}\frac{e^x-e^{-x}-2x}{x-\sin x}$]')
    # st.markdown(":green[$\sqrt{x^2+y^2}=1$] is a Pythagorean identity. :pencil:")
    # st.markdown(r'$\frac{d}{dx}(e^x + e^{-x} - 2) = e^x - e^{-x}] [\frac{d}{dx}(1 - \cos x) = \sin x$')

    # user_input = st.chat_input("    🤔 开始解题吧")

    file = st.file_uploader('上传题目图片', type=[".jpg", ".jpeg", '.png'])

    # 欢迎语
    chat_message(
        ChatMessage(generator='😘😘😘 嗨，我是你的解题小能手！\n\n **参考示例**：'),
        message_hook=lambda: st.latex(r"\lim_{x\to0}\frac{e^x-e^{-x}-2x}{x-\sin x}")
    )

    if file:
        with st.spinner('AI 正在思考🤔'):
            ocr_text = latex_ocr(file)
            # ocr_text_ = r"\lim_{x\to0}\frac{e^x-e^{-x}-2x}{x-\sin x}"
            chat_message(
                ChatMessage(generator='识别到的题目：\n\n'),
                message_hook=lambda: st.latex(ocr_text or "`未解析到具体问题`")
            )
        if ocr_text:
            with st.spinner('AI 正在解题🤔'):
                output = ai_reply(ocr_text)
                chat_message(ChatMessage(generator=output))

                # st.markdown(repr(f'{ocr_text}').strip("\'"))

            # st.markdown(_)
