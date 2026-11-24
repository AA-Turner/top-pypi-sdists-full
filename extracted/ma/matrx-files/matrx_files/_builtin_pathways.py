"""The package's own pathways — generic writers every host has.

Host features (e-signature, HR, social, brand…) declare theirs in the host
(aidream ``services/files/pathways.py``). Each entry is a DEFAULT; the live row in
``files.file_pathway`` may change its subfolder and naming.
"""

from __future__ import annotations

from .placement import register_pathway as _r

# ── The person's own files ──────────────────────────────────────────────────
_r("files.user_upload", owner_feature="files/file-service", audience="person", mode="person_chooses",
   root="my_files", naming="keep_original",
   description="A file the person uploads; lands where they put it, else My Files.",
   legacy_prefixes=("Inbox", "Uploads", "My Files/debug-uploads", "My Files/demo-pasted-images"))
_r("files.import", owner_feature="files/file-service", audience="person", root="my_files",
   subfolder="Imports/{source}", naming="keep_original",
   description="Files the person imports from another service.",
   legacy_prefixes=("Imports", "Slack Imports", "Agent Studio/Claude Imports", "Transcripts/Imports",
                    "Workbooks/Imports", "Masterwork/Chat Imports"))
_r("chat.attachment", owner_feature="chat/conversations", audience="person", root="chat_attachments",
   subfolder="{yyyy}-{mm}", naming="keep_original",
   description="Files the person attaches to a chat or an agent run.",
   legacy_prefixes=("My Files/prompt-attachments", "My Files/agent-attachments", "Chat Attachments",
                    "Shared Assets/prompt-attachments"))
_r("media.image_generation", owner_feature="media/image-generation", audience="person", root="images",
   subfolder="Generated", naming="prompt_slug_hash", system_folder="ai_images",
   description="Images the person asks an AI to make.",
   legacy_prefixes=("generations/images", "Images/Generated/image-studio"))
_r("media.audio_generation", owner_feature="media/audio", audience="person", root="audio",
   subfolder="Generated", naming="prompt_slug_hash", system_folder="ai_audio",
   description="Speech, music and sound the person asks an AI to make.",
   legacy_prefixes=("generations/audio",))
_r("media.video_generation", owner_feature="media/video", audience="person", root="video",
   subfolder="Generated", naming="prompt_slug_hash", system_folder="ai_video",
   description="Videos the person asks an AI to make.", legacy_prefixes=("generations/video",))
_r("documents.generation", owner_feature="documents/generation", audience="person", root="documents",
   subfolder="Generated", naming="prompt_slug_hash", system_folder="ai_documents",
   description="Documents the person asks an AI to write.", legacy_prefixes=("generations/documents",))
_r("audio.recording", owner_feature="media/audio", audience="person", root="audio",
   subfolder="Recordings", naming="timestamp", naming_pattern="Recording {yyyy}-{mm}-{dd} {HH}.{MI}",
   description="A recording the person deliberately makes on its page.",
   legacy_prefixes=("Audio/Recordings",))
_r("video.recording", owner_feature="media/video", audience="person", root="video",
   subfolder="Recordings", naming="timestamp", naming_pattern="Recording {yyyy}-{mm}-{dd} {HH}.{MI}",
   description="A screen or camera recording the person deliberately makes.",
   legacy_prefixes=("Video/Recordings",))

# A document the person deliberately uploads is THEIRS even when they upload it to a tool (PDF
# extractor, scanner, importer); only what the machine makes from it (text, page renders, OCR,
# derived PDFs, thumbnails) is automated (lead's application of ruling 2, 2026-10-31 — VISION).
_r("pdf.upload", owner_feature="files/pdf", audience="person", root="documents",
   subfolder="PDF uploads", naming="keep_original",
   description="A PDF the person uploads to the PDF extractor; the original stays theirs.",
   legacy_prefixes=("pdf-extractions", "system-files/pdf-extractions"))

# ── System: what the platform files on its own, and side effects ────────────
_A = dict(audience="automated", root="system")
_r("files.variant", owner_feature="files/file-service", subfolder="variants/{master}", naming="id_only",
   system_folder="variants", description="Resized and converted copies of a file.", **_A)
_r("files.thumbnail", owner_feature="files/file-service", subfolder="thumbnails", naming="id_only",
   system_folder="thumbnails", description="Preview thumbnails for the file browser.", **_A)
_r("files.preview", owner_feature="files/file-service", subfolder="previews", naming="id_only",
   system_folder="previews", description="Short-lived preview renders.", **_A)
_r("files.redaction", owner_feature="files/file-service", subfolder="redaction", naming="id_only",
   system_folder="redaction", description="Copies with personal data blacked out.", **_A)
_r("files.analysis", owner_feature="files/file-service", subfolder="analysis", naming="id_only",
   system_folder="analysis_results", description="What file analysis found, per detector.", **_A)
_r("scraper.capture", owner_feature="web/scraper", subfolder="scraper/{source}", naming="source_timestamp",
   naming_pattern="{source} {yyyy}-{mm}-{dd} {HH}.{MI}.{SS}", system_folder="scraper",
   description="Page snapshots and screenshots the scraper saves.", legacy_prefixes=("system-files/scraper",), **_A)
_r("cloud_browser.page_state", owner_feature="automation/cloud-browser", subfolder="browser-captures",
   naming="id_only", system_folder="browser_capture",
   description="Before and after screenshots around an agent's sign-in.", **_A)
_r("pdf.page_render", owner_feature="files/pdf", subfolder="page-renders", naming="id_only",
   system_folder="page_renders", description="PDF pages drawn as images for reading and OCR.", **_A)
_r("pdf.derivative", owner_feature="files/pdf", subfolder="pdf-derivatives", naming="id_only",
   system_folder="pdf_derivatives", description="Split, merged and compressed copies of a PDF.", **_A)
_r("pdf.extraction", owner_feature="files/pdf", subfolder="pdf-extractions", naming="id_only",
   system_folder="pdf_extractions", description="Text and data the machine pulls out of a PDF.", **_A)
_r("pdf.page_pdf", owner_feature="files/pdf", subfolder="pdf-page-pdfs", naming="id_only",
   system_folder="pdf_page_pdfs", description="Single pages cut from a PDF for an agent.", **_A)
_r("office.pdf_conversion", owner_feature="files/pdf", subfolder="office-pdfs", naming="id_only",
   system_folder="office_pdfs", description="PDF copies of Word, Excel and PowerPoint files.", **_A)
_r("media.audio_extract", owner_feature="media/video", subfolder="audio-extracts", naming="id_only",
   system_folder="audio_extracts", description="Sound tracks pulled out of a video.", **_A)
_r("audio.dictation", owner_feature="media/audio", subfolder="transcripts", naming="timestamp",
   naming_pattern="Dictation {yyyy}-{mm}-{dd} {HH}.{MI}.{SS}", system_folder="transcript_recordings",
   description="Audio and transcripts of voice input to an AI — a side effect.", **_A)
_r("billing.request_snapshot", owner_feature="billing/usage", subfolder="request-snapshots", naming="id_only",
   system_folder="request_snapshots", description="Byte evidence kept for a paid request.", **_A)
_r("voice.sample", owner_feature="media/audio", subfolder="voice-samples", naming="keep_original",
   system_folder="voice_samples", file_access="public", description="Voice catalog preview clips.", **_A)

# ── Temporary ───────────────────────────────────────────────────────────────
_T = dict(audience="automated", root="temp")
_r("files.upload_staging", owner_feature="files/file-service", subfolder="uploads", naming="id_only",
   description="Upload pieces waiting to be joined.", **_T)
_r("audio.chunk_journal", owner_feature="media/audio", subfolder="transcripts", naming="keep_original",
   description="Recording pieces saved while recording, for recovery.",
   legacy_prefixes=("Inbox/chunk_rec_",), **_T)
