"""
VideoUnderstanding Component.

This component uses the LLMClient interface to process videos row by row
using a specialized AI model (Google Gemini) for video understanding.
"""
from typing import Optional
from collections.abc import Callable
import asyncio
from pathlib import Path
from flowtask.interfaces.LLMClient import LLMClient
from flowtask.components import FlowComponent
from flowtask.exceptions import ConfigError

class VideoUnderstanding(LLMClient, FlowComponent):
    """
    VideoUnderstanding Component.
    
    Processes videos using Google's Gemini LLM row by row.
    Accepts a video column from the dataframe and a prompt file containing the question.

    Configuration Example:

        ```yaml
        VideoUnderstanding:
          analysis_method: "video_understanding"
          prompt_file: "questions/inventory_check.txt"
          video_column: "local_video_path"
          output_column: "video_analysis"
        ```

    Attributes:
        analysis_method: Method to use for video analysis (default: 'video_understanding' or 'image_understanding').
        prompt_file: Path to a markdown/text file containing the question/prompt.
        prompt: Direct text for the prompt (overrides prompt_file).
        video_column: The DataFrame column containing the path to the video.
        output_column: Column name for storing results (default: 'analysis_result').
    """
    def __init__(
        self,
        *args,
        job: Callable = None,
        loop: asyncio.AbstractEventLoop = None,
        analysis_method: Optional[str] = None,
        **kwargs
    ):
        # Override with our specific hardcoded parameters
        kwargs['client'] = 'google'
        kwargs['method'] = analysis_method or 'video_understanding'
        kwargs['mode'] = 'row_by_row'
        
        # User defined parameters
        self.output_column = kwargs.get('output_column', 'analysis_result')
        self.video_column = kwargs.get('video_column')
        self.prompt_file = kwargs.get('prompt_file')
        self.prompt_text = kwargs.get('prompt')
        
        # We need to set output_column in kwargs because LLMClient.__init__ will read it
        kwargs['output_column'] = self.output_column

        # Fixed parameters for video_understanding
        kwargs['method_params'] = {
            "as_image": True
        }
        
        # We will populate this in start() once we have the prompt string loaded
        kwargs['column_mapping'] = {}

        # Initialize both LLMClient and FlowComponent
        super(VideoUnderstanding, self).__init__(job, loop=loop, *args, **kwargs)

    async def start(self, **kwargs):
        """
        Initialize the VideoUnderstanding component.
        """
        # 1. Validate mandatory user inputs
        if not self.video_column:
            raise ConfigError(
                f"{self.__name__}: 'video_column' is required."
            )
            
        # 2. Get the prompt text
        if self.prompt_text:
            prompt = self.prompt_text
        elif self.prompt_file:
            # We use self.open_file if provided by FlowComponent/TaskStorage, else standard Path
            try:
                if hasattr(self, 'open_file'):
                    prompt = await self.open_file(self.prompt_file)
                else:
                    path = Path(self.prompt_file)
                    if not path.exists():
                        raise FileNotFoundError(f"Prompt file not found: {self.prompt_file}")
                    with open(path, 'r', encoding='utf-8') as f:
                        prompt = f.read()
            except Exception as e:
                raise ConfigError(
                    f"{self.__name__}: Failed to read prompt_file: {e}"
                ) from e
        else:
            raise ConfigError(
                f"{self.__name__}: Either 'prompt' or 'prompt_file' parameter must be provided."
            )
            
        # Set the prompt in method_params
        self.method_params["prompt"] = prompt
        
        # 3. Setup the column mapping for LLMClient
        # This tells LLMClient to take the value of self.video_column 
        # from the DataFrame and pass it as the 'video' argument.
        self.column_mapping = {
            "video": self.video_column
        }
        
        # 4. Run the parent start to validate remaining LLMClient requirements
        return await super().start(**kwargs)
