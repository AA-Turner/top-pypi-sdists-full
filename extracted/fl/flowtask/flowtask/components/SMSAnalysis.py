from collections.abc import Callable
import asyncio
import pandas as pd
import orjson
from ..exceptions import DataNotFound
from .CallAnalysis import CallAnalysis


class SMSAnalysis(CallAnalysis):
    """
    SMSAnalysis.

    Overview

        The SMSAnalysis class is a component for analyzing SMS conversations
        stored as JSONB in a DataFrame column. It extends CallAnalysis and
        adapts it to read messages directly from a JSONB column instead of
        loading transcripts from files or BytesIO objects.

        Supports temporal analysis via analysis_date_column: the same session_id
        can have multiple analyses over time as the conversation progresses.

    .. code-block:: yaml

        - SMSAnalysis:
            prompt_file: prompt-sms-sentiment.txt
            llm:
              llm: google
              model: gemini-2.5-flash
              temperature: 0.4
              max_tokens: 4096
            messages_column: messages
            description_column: session_id
            analysis_date_column: analysis_date
            output_column: sms_analysis
            columns:
              - session_id
              - analysis_date
            lookup_table: sms_analysis
            lookup_schema: flexroc
            max_concurrent_calls: 5
            max_requests_per_minute: 50

    |---|---|---|
    | version | No | version of component |
    """
    _version = "1.1.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        # Set default goal for SMS analysis
        kwargs.setdefault(
            'goal',
            'Your task is to analyze SMS conversations and provide detailed sentiment and engagement analysis'
        )

        # Force dataframe mode, no file/bytes handling needed
        kwargs['use_dataframe'] = True
        kwargs['use_bytes_input'] = False

        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

        # SMS-specific parameters
        self.messages_column: str = kwargs.get('messages_column', 'messages')
        self.participants_column: str = kwargs.get('participants_column', 'participants')
        self.analysis_date_column: str = kwargs.get('analysis_date_column', None)

        # When analysis_date_column is set, repurpose lookup_schema_column
        # so bot_evaluation's build_call_key returns (analysis_date, session_id)
        if self.analysis_date_column:
            self.lookup_schema_column = self.analysis_date_column
            self.group_analysis = False  # Each (session_id, analysis_date) is unique

    def _build_participants_lookup(self, participants_json) -> tuple[dict, str | None]:
        """Build a phone_number -> display_name lookup from participants data.

        Also identifies the session owner (agent).

        Returns:
            tuple: (phone_to_name dict, agent_name or None)
        """
        phone_to_name = {}
        agent_name = None

        if participants_json is None or (isinstance(participants_json, float) and pd.isna(participants_json)):
            return phone_to_name, agent_name

        if isinstance(participants_json, str):
            try:
                participants = orjson.loads(participants_json)
            except Exception:
                return phone_to_name, agent_name
        elif isinstance(participants_json, list):
            participants = participants_json
        else:
            return phone_to_name, agent_name

        for p in participants:
            if not isinstance(p, dict):
                continue
            phone = p.get('phone_number')
            display_name = None
            is_owner = p.get('is_session_owner', False)
            owner = p.get('owner')
            if isinstance(owner, dict):
                display_name = owner.get('display_name')
                phone = phone or owner.get('phone_number')
            if phone and display_name:
                phone_to_name[phone] = display_name
            if is_owner and display_name:
                agent_name = display_name
            elif is_owner and phone:
                agent_name = phone

        return phone_to_name, agent_name

    def _extract_sender_label(self, sender: dict, phone_to_name: dict = None) -> str:
        """Extract a readable label from a sender dict.

        Handles both structures (display_name can be at sender or owner level):
          - {"owner": {"type": "user", "id": "..."}, "display_name": "...", "phone_number": "..."}
          - {"owner": {"display_name": "...", "phone_number": "..."}}
          - {"phone_number": "..."}

        Falls back to participants lookup when display_name is missing.
        """
        if not isinstance(sender, dict):
            return "?"
        # Check sender level first
        display_name = sender.get('display_name')
        phone_number = sender.get('phone_number')
        # Also check inside owner dict (some sessions nest it there)
        owner = sender.get('owner')
        if isinstance(owner, dict):
            display_name = display_name or owner.get('display_name')
            phone_number = phone_number or owner.get('phone_number')
        # Resolve from participants lookup if no display_name
        if not display_name and phone_number and phone_to_name:
            display_name = phone_to_name.get(phone_number)
        return display_name or phone_number or "?"

    def _extract_recipients_label(self, to_members, phone_to_name: dict = None) -> str:
        """Extract a readable label from the to_members list.

        Handles both structures (display_name can be at member or owner level):
          - [{"phone_number": "..."}]
          - [{"owner": {"display_name": "...", "phone_number": "..."}}]
          - [{"owner": {"type": "user"}, "display_name": "...", "phone_number": "..."}]

        Falls back to participants lookup when display_name is missing.
        """
        if not isinstance(to_members, list) or not to_members:
            return "?"
        labels = []
        for member in to_members:
            if not isinstance(member, dict):
                continue
            # Check member level first
            display_name = member.get('display_name')
            phone_number = member.get('phone_number')
            # Also check inside owner dict
            owner = member.get('owner')
            if isinstance(owner, dict):
                display_name = display_name or owner.get('display_name')
                phone_number = phone_number or owner.get('phone_number')
            # Resolve from participants lookup if no display_name
            if not display_name and phone_number and phone_to_name:
                display_name = phone_to_name.get(phone_number)
            label = display_name or phone_number
            if label:
                labels.append(label)
        return ", ".join(labels) if labels else "?"

    def _format_messages_as_conversation(self, messages_json, participants_json=None) -> str:
        """
        Convert JSONB messages to a readable conversation text for the LLM.

        Uses participants data (when available) to resolve phone numbers to
        display names and identify the session owner (agent).

        Handles the real JSONB structure from flexroc.sms:
          {
            "date_time": "2026-01-02T21:34:14Z",
            "direction": "Out",
            "sender": {"owner": {"display_name": "Alvaro Lopez", "phone_number": "178..."}},
            "to_members": [{"phone_number": "125..."}],
            "message": "Hi LaTisha..."
          }

        Returns:
            str: Formatted conversation text, or empty string on failure.
        """
        if messages_json is None or (isinstance(messages_json, float) and pd.isna(messages_json)):
            return ""

        # Build phone->name lookup from participants
        phone_to_name, agent_name = self._build_participants_lookup(participants_json)

        # Parse JSON string if needed
        if isinstance(messages_json, str):
            try:
                messages = orjson.loads(messages_json)
            except Exception:
                return ""
        elif isinstance(messages_json, list):
            messages = messages_json
        else:
            return ""

        if not messages:
            return ""

        # Sort by date_time if available
        try:
            messages = sorted(
                messages,
                key=lambda m: m.get('date_time', '') or ''
            )
        except (TypeError, AttributeError):
            pass

        lines = []

        # Prepend participants context if available
        if phone_to_name:
            participant_lines = []
            for phone, name in phone_to_name.items():
                role = "(Agent/Owner)" if name == agent_name else "(Contact)"
                participant_lines.append(f"  - {name} ({phone}) {role}")
            if participant_lines:
                lines.append("PARTICIPANTS:")
                lines.extend(participant_lines)
                lines.append("")

        for msg in messages:
            if not isinstance(msg, dict):
                continue

            direction = msg.get('direction', '?')
            date_time = msg.get('date_time', '')
            text_content = msg.get('message', '') or msg.get('text', '') or msg.get('body', '') or ''

            # Extract sender and recipients, resolving from participants lookup
            from_label = self._extract_sender_label(msg.get('sender', {}), phone_to_name)
            to_label = self._extract_recipients_label(msg.get('to_members', []), phone_to_name)

            timestamp = f"[{date_time}] " if date_time else ""
            lines.append(
                f"{timestamp}{direction.upper()} ({from_label} -> {to_label}): {text_content}"
            )

        return "\n".join(lines)

    async def start(self, **kwargs):
        """
        Start the SMSAnalysis component.

        Receives a DataFrame from the previous component, validates that
        messages_column exists, and converts the JSONB messages into
        formatted conversation text in content_column.
        """
        if self.previous:
            self.data = self.input

        # Call the grandparent start (ParrotBot + FlowComponent),
        # skipping CallAnalysis.start() file/bytes logic
        from ..interfaces.ParrotBot import ParrotBot
        await ParrotBot.start(self, **kwargs)

        # Normalize dict inputs (multi-schema outputs) into a single DataFrame
        if isinstance(self.data, dict):
            frames = []
            for schema_key, df_val in self.data.items():
                if not isinstance(df_val, pd.DataFrame):
                    continue
                df_local = df_val
                if self.lookup_schema_column and self.lookup_schema_column not in df_local.columns:
                    df_local = df_local.copy()
                    df_local[self.lookup_schema_column] = schema_key
                frames.append(df_local)
            if not frames:
                raise DataNotFound(
                    f"{self._bot_name.lower()}: expected DataFrame input but got dict without DataFrames."
                )
            self.data = pd.concat(frames, ignore_index=True)
            self._logger.info(
                f"{self._bot_name.lower()}: flattened dict input into dataframe with {len(self.data)} rows"
            )

        # Validate messages_column exists
        if self.messages_column not in self.data.columns:
            if self.skip_existing and self.output_column in self.data.columns:
                rows_needing_processing = self.data[self.output_column].isna().sum()
                if rows_needing_processing == 0:
                    self._logger.info(
                        f"All {len(self.data)} rows already have '{self.output_column}'. "
                        f"Skipping '{self.messages_column}' validation."
                    )
                else:
                    raise DataNotFound(
                        f"{self._bot_name.lower()}: messages_column '{self.messages_column}' "
                        f"not found in data columns. {rows_needing_processing} rows need processing."
                    )
            else:
                raise DataNotFound(
                    f"{self._bot_name.lower()}: messages_column '{self.messages_column}' "
                    f"not found in data columns: {list(self.data.columns)}"
                )

        # Validate analysis_date_column if configured
        if self.analysis_date_column:
            if self.analysis_date_column not in self.data.columns:
                raise DataNotFound(
                    f"{self._bot_name.lower()}: analysis_date_column '{self.analysis_date_column}' "
                    f"not found in data columns: {list(self.data.columns)}"
                )

        # Set up columns to preserve
        if not self.columns:
            self.columns = [self._desc_column]
        else:
            if self._desc_column not in self.columns:
                self.columns.append(self._desc_column)

        # Ensure analysis_date_column is in output columns
        if self.analysis_date_column and self.analysis_date_column not in self.columns:
            self.columns.append(self.analysis_date_column)

        # Convert JSONB messages to formatted conversation text
        if self.messages_column in self.data.columns:
            self._logger.info(
                f"Formatting SMS messages from '{self.messages_column}' into '{self.content_column}'"
            )
            has_participants = self.participants_column in self.data.columns
            if has_participants:
                self._logger.info(
                    f"Using '{self.participants_column}' to resolve participant names"
                )
                self.data[self.content_column] = self.data.apply(
                    lambda row: self._format_messages_as_conversation(
                        row[self.messages_column],
                        row.get(self.participants_column)
                    ),
                    axis=1
                )
            else:
                self.data[self.content_column] = self.data[self.messages_column].apply(
                    self._format_messages_as_conversation
                )
            content_loaded = self.data[self.content_column].apply(
                lambda x: bool(x and str(x).strip())
            ).sum()
            self._logger.info(
                f"Successfully formatted {content_loaded}/{len(self.data)} SMS conversations"
            )
        else:
            self._logger.info(
                f"Skipping message formatting - will use existing '{self.output_column}' values"
            )

        # Set eval_column for bot processing
        self._eval_column = self.content_column

        return True

    def format_question(self, call_identifier, transcripts, row=None):
        """
        Format the question for SMS conversation analysis.

        Args:
            call_identifier: identifier for the conversation (e.g. session_id)
            transcripts: list of formatted conversation texts
            row: optional row data for additional context

        Returns:
            str: formatted question for the AI bot
        """
        combined_conversation = "\n\n".join([
            transcript.strip() if transcript and len(transcript) < 15000
            else (transcript[:15000] + "..." if transcript else "")
            for transcript in transcripts
        ])

        # Include analysis_date context if available
        date_context = ""
        if self.analysis_date_column and row is not None:
            analysis_date = row.get(self.analysis_date_column) if hasattr(row, 'get') else None
            if analysis_date is not None:
                date_context = f"\nAnalysis Date: {analysis_date} (analyze conversation up to this date)\n"

        question = f"""
Conversation ID: {call_identifier}
{date_context}
Please analyze the following SMS conversation and provide a detailed analysis:

SMS CONVERSATION:
{combined_conversation}

Please provide your analysis in the specified JSON format.
"""
        return question

    async def run(self):
        """
        Run the SMSAnalysis component.

        Returns:
            pandas.DataFrame: DataFrame with SMS analysis results
        """
        self._result = await self.bot_evaluation()
        self._print_data_(self._result, 'SMSAnalysis')
        return self._result

    async def close(self):
        """Close the SMSAnalysis component."""
        pass
