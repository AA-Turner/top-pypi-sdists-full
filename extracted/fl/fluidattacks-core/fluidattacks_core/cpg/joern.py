import asyncio
import logging
import os
import signal
from collections.abc import Iterable
from enum import Enum

from fluidattacks_core.filesystem import Language as SiftsLanguage

LOGGER = logging.getLogger(__name__)


class Language(Enum):
    Swift = "swiftsrc"
    CSharp = "csharpsrc"
    Go = "golang"
    FuzzyTestLang = "fuzzy_test_lang"
    Java = "javasrc"
    Python = "pythonsrc"
    PHP = "php"
    Ruby = "rubysrc"
    C = "c"
    Kotlin = "kotlin"
    Ghidra = "ghidra"
    JavaScript = "javascript"
    LLVM = "llvm"
    NewC = "newc"
    JS = "jssrc"

    CSharpAlias = "csharp"
    PythonAlias = "python"
    JavaAlias = "java"

    def __str__(self) -> str:
        """Return the string representation of the language."""
        return self.value

    @classmethod
    def from_sifts_language(cls, language: SiftsLanguage) -> "Language":
        dict_language = {
            SiftsLanguage.Swift: cls.Swift,
            SiftsLanguage.CSharp: cls.CSharp,
            SiftsLanguage.Go: cls.Go,
            SiftsLanguage.FuzzyTestLang: cls.FuzzyTestLang,
            SiftsLanguage.Java: cls.Java,
            SiftsLanguage.Python: cls.Python,
            SiftsLanguage.PHP: cls.PHP,
            SiftsLanguage.Ruby: cls.Ruby,
            SiftsLanguage.C: cls.C,
            SiftsLanguage.Kotlin: cls.Kotlin,
            SiftsLanguage.Ghidra: cls.Ghidra,
            SiftsLanguage.JavaScript: cls.JavaScript,
            SiftsLanguage.LLVM: cls.LLVM,
            SiftsLanguage.NewC: cls.NewC,
        }
        if language in dict_language:
            return dict_language[language]
        msg = f"Unsupported language: {language}"
        raise ValueError(msg)


lock = asyncio.Lock()


async def run_joern_command(cmd: str, args: Iterable[str]) -> bool:
    try:
        env = os.environ.copy()
        env["JAVA_OPTS"] = env.get("JAVA_OPTS", "") + " -Xmx4096m"
        env["_JAVA_OPTS"] = env.get("_JAVA_OPTS", "") + " -Xmx4096m"
        async with lock:
            proc = await asyncio.create_subprocess_exec(
                cmd,
                *args,
                stdout=None,
                stderr=asyncio.subprocess.PIPE,
                env=env,
            )
            _, stderr = await proc.communicate()

        if proc.returncode != 0 and stderr.decode().strip():
            LOGGER.error("Running %s with args %s", cmd, " ".join(args))
            LOGGER.error(stderr.decode().strip())
            return False

        return True  # noqa: TRY300
    except TimeoutError:
        os.killpg(proc.pid, signal.SIGKILL)
        LOGGER.exception("Command %s timed out after 3 minutes", cmd)
        return False
