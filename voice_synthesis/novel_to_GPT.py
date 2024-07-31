# %%
import sys
from openai import OpenAI, AssistantEventHandler


#api_key and content预先定义做测试用
api_key="you-key"
content="""
  第49章 两小无猜一大傻
书名：不让江山作者名：知白本章字数：3332字更新时间：2020-09-12 13:28:31
羽亲王殿下亲自到了教习小食堂那边去请教食堂师傅们饭菜做法，以他的身份，自然不会有谁阻拦，倒是把那些食堂师傅吓着了，一个个脸色惶恐不安。

夏侯琢很开心，他这样的人对他父亲说两三句狠话，便是最后的骄傲和自尊，也是他对亲人狠厉的极限。

可实际上，在他父亲面前，他的伪装并不好。

身份带来了诸多便利，别人苦求都办不到的事，亲王一言就可轻松做到。

比如夏侯琢说他想看父亲做饭是什么样子，而羽亲王觉得夏侯琢现在身上有伤，进厨房会被油烟呛着，所以问了一句能不能把炊具之类的东西搬到燕青之的小院里。

他问一句，哪有人会说不行的。

于是小厨房那边的人全都忙活起来，锅碗瓢盆油盐酱醋，一股脑的往燕青之的小院里搬，还用最短的时间搭起来一个土灶，大铁锅已经刷的干干净净。

燕青之和李丢丢拎着修好的木桶回来，看到小院里这热闹的样子两个人都懵了一下。

“我的菜！”
  """

# Capture command-line arguments
api_key = sys.argv[1] if len(sys.argv) > 2 else ''
content = sys.argv[2] if len(sys.argv) > 2 else ''
# print(api_key)
# print(content)
# Initialize OpenAI client with the provided API key
client = OpenAI(api_key=api_key)

# Define the assistant with necessary instructions
assistant = client.beta.assistants.create(
    name="Novel scriptify",
    instructions="""
用户会提供一段小说，先找出有几个角色有台词（包括旁白，提到名字的人物但没有台词的不算）并猜测每个角色的性别。
格式为：
##登场角色

###角色1：旁白，男声
###角色2：女1，女声
###角色3：男1，男声

列举完成后空一行，输出以下一行：
##小说台词本

然后把小说改成台词本的形式，开头的标题、作者信息是属于旁白的台词。每段台词都标注语气：
1=轻急，用于恍然大悟，自言自语等语气；
2=轻缓，用于虚弱、无力、沉吟等语气；
3=中性，用于中性语气；
4=重缓，用于质问，威胁，强调、调侃等语气；
5=重急，用于危急，焦急，不耐烦等语气。
旁白的语气多数用3，可以少量用其他语气。其他角色的语气请正常分配。每一段台词的格式：
**角色名字**:(语气数字)台词
一段台词中间的空格和换行符都替换成句号。如果一段台词超过3句话，请拆拆成多段。

分个几个场景，不要超过5个，标注每个场景适合什么类型背景音乐。场景音乐类型：
1=轻急，用于轻松愉快的场景；
2=轻缓，用于悲凉的场景；
3=中性，用于一般场景；
4=重缓，用于高潮来临前，恐怖来袭的紧张场景；
5=重急，用于飙车、战斗高潮等场景。
场景的格式：
### 场景一:(语气数字)[轻松愉快的背景音乐]教习小食堂

你只需完成以上任务，不要续写小说内容！！
以纯文本形式回答。
""",
    model="gpt-4o",
)

# Create a new thread for the conversation
thread = client.beta.threads.create()

# Send the content provided by the user to the assistant
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=content,
)

# Define a custom event handler
class EventHandler(AssistantEventHandler):    
    def on_text_created(self, text) -> None:
        self.display_text(text)
      
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)
      
    def on_tool_call_created(self, tool_call):
        print(f"{tool_call.type}\n", flush=True)
  
    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)
    
    def display_text(self, text):
        # Filter out annotations or other metadata
        if isinstance(text, str):
            print(text, end="", flush=True)
        elif hasattr(text, 'value'):
            # If the text has a 'value' attribute, print its content
            print(text.value, end="", flush=True)


# Stream the assistant's response using the custom event handler
with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    event_handler=EventHandler(),
) as stream:
    stream.until_done()
