# """Test cases for Power Point interface."""

# import pytest
# from bacore.interfaces.power_point import SPresentation, SSlide
# from pathlib import Path
# from sqlmodel import Session, SQLModel, create_engine

# sqlite_file_path = "data/database.db"
# sqlite_url = f"sqlite:///{sqlite_file_path}"

# engine = create_engine(sqlite_url, echo=True)


# def create_presentation_data():
#     with Session(engine) as session:
#         bacore_main_content = SSlide(title="Main Content")
#         session.add(bacore_main_content)

#         bacore_presentation = SPresentation(
#             name="BACore Presentation",
#             slides=[SSlide(title="Introduction"), bacore_main_content],
#         )
#         session.add(bacore_presentation)
#         session.commit()
#         session.refresh(bacore_main_content)
#         session.refresh(bacore_presentation)
#         return bacore_presentation


# @pytest.mark.skip
# def test_spresentation():
#     if Path(sqlite_file_path).exists():
#         Path(sqlite_file_path).unlink()
#     assert not Path(sqlite_file_path).exists(), "The presentation file was not reset."

#     SQLModel.metadata.create_all(engine)
#     bacore_presentation = create_presentation_data()
#     assert bacore_presentation.id == 1
#     assert bacore_presentation.name == "BACore Presentation"
#     assert bacore_presentation.slides == SSlide()
