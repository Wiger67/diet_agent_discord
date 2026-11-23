from langchain.agents import create_agent 
from dotenv import load_dotenv
load_dotenv()
SHOW_STEPS = True   # 看過程 True , 只看答案 False

agent = create_agent(
    model="claude-haiku-5-5",
    tools=[],
    system_prompt=(
        "你是飲食控制助理，用繁體中文回答。看照片列出每樣食物、估計克數和熱量，最後給總熱量。估計值要說是估計，看不到食物就直接說"
    )
)




if __name__ == "__main__":
    questions = [
    "早餐吃了一個鮪魚飯糰和一瓶無糖豆漿，大概多少熱量？",
    "午餐是排骨便當，飯吃一半",
    "我想一天只吃 800 卡，可以嗎？",   # 應該不配合
    "你好",                             # 應該正常回答，不硬算熱量
    "今天天氣如何？",                   # 超出範圍，應該說做不到
    ]

    for question in questions:
        print("=" * 40)
        print("問題：", question)
        result = agent.invoke({"messages": [{"role": "user", "content": question}]})

        if SHOW_STEPS:
            # 印出每一則訊息：使用者、模型、工具回傳（接上工具後會看到 ToolMessage）
            for msg in result["messages"]:
                print(type(msg).__name__, "->", msg.text)
        else:
            print(result["messages"][-1].text)


