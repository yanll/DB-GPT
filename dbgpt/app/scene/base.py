from enum import Enum
from typing import List, Optional

from dbgpt._private.pydantic import BaseModel, Field
from dbgpt.core import BaseOutputParser, ChatPromptTemplate
from dbgpt.core._private.example_base import ExampleSelector


class Scene:
    def __init__(
        self,
        code,
        name,
        describe,
        param_types: List = [],
        is_inner: bool = False,
        show_disable=False,
        prepare_scene_code: str = None,
    ):
        self.code = code
        self.name = name
        self.describe = describe
        self.param_types = param_types
        self.is_inner = is_inner
        self.show_disable = show_disable
        self.prepare_scene_code = prepare_scene_code


class ChatScene(Enum):
    ChatWithDbExecute = Scene(
        code="chat_with_db_execute",
        name="Chat Data",
        describe="通过自然语言对话对数据进行查询和分析",
        param_types=["DB Select"],
    )
    ExcelLearning = Scene(
        code="excel_learning",
        name="Excel Learning",
        describe="统计分析您上传的Excel文件数据",
        is_inner=True,
    )
    ChatExcel = Scene(
        code="chat_excel",
        name="Chat Excel",
        describe="通过自然语言对话分析Excel文件",
        param_types=["File Select"],
        prepare_scene_code="excel_learning",
    )

    ChatWithDbQA = Scene(
        code="chat_with_db_qa",
        name="Chat DB",
        describe="通过自然语言对话检索元数据",
        param_types=["DB Select"],
    )
    ChatExecution = Scene(
        code="chat_execution",
        name="Use Plugin",
        describe="使用内置插件",
        param_types=["Plugin Select"],
    )

    ChatAgent = Scene(
        code="chat_agent",
        name="Agent Chat",
        describe="使用对话代理工具",
        param_types=["Plugin Select"],
    )

    ChatFlow = Scene(
        code="chat_flow",
        name="Flow Chat",
        describe="通过AWEL工作流编排实现业务目标",
        param_types=["Flow Select"],
    )

    InnerChatDBSummary = Scene(
        "inner_chat_db_summary", "DB Summary", "Db Summary.", True
    )

    ChatNormal = Scene(
        "chat_normal", "Chat Normal", "Native LLM large model AI dialogue."
    )
    ChatDashboard = Scene(
        "chat_dashboard",
        "Dashboard",
        "基于自然语言对话生成数据报表、仪表板",
        ["DB Select"],
    )
    ChatKnowledge = Scene(
        "chat_knowledge",
        "Chat Knowledge",
        "基于文档和知识库的自然语言对话",
        ["Knowledge Space Select"],
    )
    ExtractTriplet = Scene(
        "extract_triplet",
        "Extract Triplet",
        "Extract Triplet",
        ["Extract Select"],
        True,
    )
    ExtractSummary = Scene(
        "extract_summary",
        "Extract Summary",
        "Extract Summary",
        ["Extract Select"],
        True,
    )
    ExtractRefineSummary = Scene(
        "extract_refine_summary",
        "Extract Summary",
        "Extract Summary",
        ["Extract Select"],
        True,
    )
    ExtractEntity = Scene(
        "extract_entity", "Extract Entity", "Extract Entity", ["Extract Select"], True
    )
    QueryRewrite = Scene(
        "query_rewrite", "query_rewrite", "query_rewrite", ["query_rewrite"], True
    )

    @staticmethod
    def of_mode(mode):
        return [x for x in ChatScene if mode == x.value()][0]

    @staticmethod
    def is_valid_mode(mode):
        return any(mode == item.value() for item in ChatScene)

    def value(self):
        return self._value_.code

    def scene_name(self):
        return self._value_.name

    def describe(self):
        return self._value_.describe

    def param_types(self):
        return self._value_.param_types

    def show_disable(self):
        return self._value_.show_disable

    def is_inner(self):
        return self._value_.is_inner


class AppScenePromptTemplateAdapter(BaseModel):
    """The template of the scene.

    Include some fields that in :class:`dbgpt.core.PromptTemplate`
    """

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    prompt: ChatPromptTemplate = Field(..., description="The prompt of this scene")
    template_scene: Optional[str] = Field(
        default=None, description="The scene of this template"
    )
    template_is_strict: Optional[bool] = Field(
        default=True, description="Whether strict"
    )

    output_parser: Optional[BaseOutputParser] = Field(
        default=None, description="The output parser of this scene"
    )
    sep: Optional[str] = Field(
        default="###", description="The default separator of this scene"
    )

    stream_out: Optional[bool] = Field(
        default=True, description="Whether to stream out"
    )
    example_selector: Optional[ExampleSelector] = Field(
        default=None, description="Example selector"
    )
    need_historical_messages: Optional[bool] = Field(
        default=False, description="Whether to need historical messages"
    )
    temperature: Optional[float] = Field(
        default=0.6, description="The default temperature of this scene"
    )
    max_new_tokens: Optional[int] = Field(
        default=1024, description="The default max new tokens of this scene"
    )
    str_history: Optional[bool] = Field(
        default=False, description="Whether transform history to str"
    )
