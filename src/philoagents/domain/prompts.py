import opik
from loguru import logger


class Prompt:
    def __init__(self, name: str, prompt: str) -> None:
        self.name = name

        try:
            self.__prompt = opik.Prompt(name=name, prompt=prompt)
        except Exception:
            logger.warning(
                "Can't use Opik to version the prompt (probably due to missing or invalid credentials). Falling back to local prompt. The prompt is not versioned, but it's still usable."
            )

            self.__prompt = prompt

    @property
    def prompt(self) -> str:
        if isinstance(self.__prompt, opik.Prompt):
            return self.__prompt.prompt
        else:
            return self.__prompt

    def __str__(self) -> str:
        return self.prompt

    def __repr__(self) -> str:
        return self.__str__()


# ===== PROMPTS =====

# --- Philosophers ---

__PHILOSOPHER_CHARACTER_CARD = """
دعنا نتظاهر. أنت {{philosopher_name}} - شخص حقيقي، تشارك في حوار فلسفي مع فرد آخر.
استخدم جملاً قصيرة، اشرح أفكارك ووجهة نظرك بطريقة موجزة لكن تعليمية وجذابة. لا يجب أن تتجاوز ردودك مائة كلمة.

اسمك ووجهة نظرك الفلسفية وأسلوب حديثك مفصلة أدناه.

---

اسم الفيلسوف: {{philosopher_name}}
المنظور الفلسفي: {{philosopher_perspective}}
أسلوب الحديث: {{philosopher_style}}

---

يجب عليك دائماً اتباع هذه القواعد:

- لن تذكر أبداً أنك ذكاء اصطناعي أو مساعد افتراضي.
- إذا كانت هذه المرة الأولى التي تتحدث فيها مع المستخدم، يجب أن تقدم نفسك.
- قدم ردوداً نصية بسيطة بدون مؤشرات تنسيق أو تعليقات وصفية.
- تأكد دائماً من عدم تجاوز ردك 80 كلمة.
- رد دائماً باللغة العربية حتى لو كان المستخدم يتحدث بلغة أخرى. العربية فقط.

---

ملخص المحادثة السابقة بين {{philosopher_name}} والمستخدم:

{{summary}}

---

يبدأ الحوار بين {{philosopher_name}} والمستخدم الآن.
"""

PHILOSOPHER_CHARACTER_CARD = Prompt(
    name="philosopher_character_card",
    prompt=__PHILOSOPHER_CHARACTER_CARD,
)

# --- Summary ---

__SUMMARY_PROMPT = """أنشئ ملخصاً للمحادثة بين {{philosopher_name}} والمستخدم.
يجب أن يكون الملخص وصفاً موجزاً للمحادثة حتى الآن، لكنه يجب أن يلتقط جميع المعلومات ذات الصلة المشتركة بين {{philosopher_name}} والمستخدم: """

SUMMARY_PROMPT = Prompt(
    name="summary_prompt",
    prompt=__SUMMARY_PROMPT,
)

__EXTEND_SUMMARY_PROMPT = """هذا ملخص للمحادثة حتى الآن بين {{philosopher_name}} والمستخدم:

{{summary}}

وسّع الملخص من خلال الأخذ في الاعتبار الرسائل الجديدة أعلاه: """

EXTEND_SUMMARY_PROMPT = Prompt(
    name="extend_summary_prompt",
    prompt=__EXTEND_SUMMARY_PROMPT,
)

__CONTEXT_SUMMARY_PROMPT = """مهمتك هي تلخيص المعلومات التالية إلى أقل من 50 كلمة. فقط أرجع الملخص، لا تضمن أي نص آخر:

{{context}}"""

CONTEXT_SUMMARY_PROMPT = Prompt(
    name="context_summary_prompt",
    prompt=__CONTEXT_SUMMARY_PROMPT,
)

# --- Evaluation Dataset Generation ---

__EVALUATION_DATASET_GENERATION_PROMPT = """
أنشئ محادثة بين فيلسوف ومستخدم بناءً على الوثيقة المقدمة. سيرد الفيلسوف على أسئلة المستخدم بالإشارة إلى الوثيقة. إذا كان السؤال غير مرتبط بالوثيقة، سيرد الفيلسوف بـ 'لا أعرف.'

يجب أن تكون المحادثة بصيغة JSON التالية:

{
    "messages": [
        {"role": "user", "content": "مرحباً اسمي <user_name>. <سؤال_مرتبط_بالوثيقة_ووجهة_نظر_الفيلسوف> ؟"},
        {"role": "assistant", "content": "<ردّ_الفيلسوف>"},
        {"role": "user", "content": "<سؤال_مرتبط_بالوثيقة_ووجهة_نظر_الفيلسوف> ؟"},
        {"role": "assistant", "content": "<ردّ_الفيلسوف>"},
        {"role": "user", "content": "<سؤال_مرتبط_بالوثيقة_ووجهة_نظر_الفيلسوف> ؟"},
        {"role": "assistant", "content": "<ردّ_الفيلسوف>"}
    ]
}

أنشئ بحد أقصى 4 أسئلة وأجوبة وبحد أدنى 2 أسئلة وأجوبة. تأكد من أن ردود الفيلسوف تعكس بدقة محتوى الوثيقة.

الفيلسوف: {{philosopher}}
الوثيقة: {{document}}

ابدأ المحادثة برسالة من المستخدم، ثم أنشئ رد الفيلسوف بناءً على الوثيقة. استمر في المحادثة مع طرح المستخدم أسئلة متابعة ورد الفيلسوف عليها وفقاً لذلك.

يجب عليك الانتباه إلى ما يلي:

- ابدأ دائماً المحادثة بتقديم المستخدم (على سبيل المثال، 'مرحباً اسمي صوفيا') ثم بسؤال يتعلق بالوثيقة ووجهة نظر الفيلسوف.
- أنشئ دائماً أسئلة كما لو كان المستخدم يتحدث مباشرة مع الفيلسوف باستخدام ضمائر مثل 'أنت' أو 'لك'، محاكاة حوار حقيقي يحدث في الوقت الفعلي.
- سيرد الفيلسوف على أسئلة المستخدم بناءً على الوثيقة.
- سيطرح المستخدم على الفيلسوف أسئلة حول الوثيقة وملف تعريف الفيلسوف.
- إذا كان السؤال غير مرتبط بالوثيقة، سيقول الفيلسوف أنه لا يعرف.
- رد دائماً باللغة العربية الفصحى. العربية فقط!
"""

EVALUATION_DATASET_GENERATION_PROMPT = Prompt(
    name="evaluation_dataset_generation_prompt",
    prompt=__EVALUATION_DATASET_GENERATION_PROMPT,
)
