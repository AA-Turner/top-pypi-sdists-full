# Standard Library
from unittest.mock import patch

# AA Killstats
from killstats.helpers import eveonline
from killstats.tests import NoSocketsTestCase

MODULE_PATH = "killstats.helpers.eveonline"


class TestEVEOnlineHelper(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

    @patch(f"{MODULE_PATH}.character_portrait_url")
    def test_get_character_portrait_url_should_return_url(
        self, mock_character_portrait_url
    ):
        # Test Data
        mock_character_portrait_url.return_value = (
            "https://images.example/characters/1001"
        )
        # Test Action
        result = eveonline.get_character_portrait_url(character_id=1001, size=64)
        # Expected Result
        self.assertEqual(result, "https://images.example/characters/1001")
        mock_character_portrait_url.assert_called_once_with(character_id=1001, size=64)

    @patch(f"{MODULE_PATH}.character_portrait_url")
    def test_should_return_empty_for_invalid_input(self, mock_character_portrait_url):
        # Test Data
        mock_character_portrait_url.side_effect = ValueError("invalid character id")
        # Test Action
        result = eveonline.get_character_portrait_url(character_id=0)
        # Expected Result
        self.assertEqual(result, "")
        mock_character_portrait_url.assert_called_once_with(character_id=0, size=32)

    @patch(f"{MODULE_PATH}.character_portrait_url")
    def test_should_return_html_for_character_portrait(
        self, mock_character_portrait_url
    ):
        # Test Data
        mock_character_portrait_url.return_value = (
            "https://images.example/characters/1001"
        )
        # Test Action
        result = eveonline.get_character_portrait_url(
            character_id=1001,
            size=64,
            character_name="Bruce Wayne",
            as_html=True,
        )
        # Expected Result
        self.assertEqual(
            str(result),
            '<img class="character-portrait rounded-circle" src="https://images.example/characters/1001" alt="Bruce Wayne">',
        )

    @patch(f"{MODULE_PATH}.corporation_logo_url")
    def test_should_return_url_for_corporation_logo(self, mock_corporation_logo_url):
        # Test Data
        mock_corporation_logo_url.return_value = (
            "https://images.example/corporations/2001"
        )
        # Test Action
        result = eveonline.get_corporation_logo_url(corporation_id=2001, size=128)
        # Expected Result
        self.assertEqual(result, "https://images.example/corporations/2001")
        mock_corporation_logo_url.assert_called_once_with(corporation_id=2001, size=128)

    @patch(f"{MODULE_PATH}.corporation_logo_url")
    def test_should_return_html_for_corporation_logo(self, mock_corporation_logo_url):
        # Test Data
        mock_corporation_logo_url.return_value = (
            "https://images.example/corporations/2001"
        )
        # Test Action
        result = eveonline.get_corporation_logo_url(
            corporation_id=2001,
            size=128,
            corporation_name="Wayne Technologies",
            as_html=True,
        )
        # Expected Result
        self.assertEqual(
            str(result),
            '<img class="corporation-logo rounded-circle" src="https://images.example/corporations/2001" alt="Wayne Technologies">',
        )

    @patch(f"{MODULE_PATH}.alliance_logo_url")
    def test_should_return_url_for_alliance_logo(self, mock_alliance_logo_url):
        # Test Data
        mock_alliance_logo_url.return_value = "https://images.example/alliances/3001"
        # Test Action
        result = eveonline.get_alliance_logo_url(alliance_id=3001, size=256)
        # Expected Result
        self.assertEqual(result, "https://images.example/alliances/3001")
        mock_alliance_logo_url.assert_called_once_with(alliance_id=3001, size=256)

    @patch(f"{MODULE_PATH}.alliance_logo_url")
    def test_should_return_html_for_alliance_logo(self, mock_alliance_logo_url):
        # Test Data
        mock_alliance_logo_url.return_value = "https://images.example/alliances/3001"
        # Test Action
        result = eveonline.get_alliance_logo_url(
            alliance_id=3001,
            size=256,
            alliance_name="Wayne Enterprises",
            as_html=True,
        )
        # Expected Result
        self.assertEqual(
            str(result),
            '<img class="alliance-logo rounded-circle" src="https://images.example/alliances/3001" alt="Wayne Enterprises">',
        )

    @patch(f"{MODULE_PATH}.type_render_url")
    def test_should_return_url_for_type_render(self, mock_type_render_url):
        # Test Data
        mock_type_render_url.return_value = "https://images.example/types/4001/render"
        # Test Action
        result = eveonline.get_type_render_url(type_id=4001, size=64)
        # Expected Result
        self.assertEqual(result, "https://images.example/types/4001/render")
        mock_type_render_url.assert_called_once_with(type_id=4001, size=64)

    @patch(f"{MODULE_PATH}.type_render_url")
    def test_should_return_html_for_type_render(self, mock_type_render_url):
        # Test Data
        mock_type_render_url.return_value = "https://images.example/types/4001/render"
        # Test Action
        result = eveonline.get_type_render_url(
            type_id=4001,
            size=64,
            type_name="Rifter",
            as_html=True,
        )
        # Expected Result
        self.assertEqual(
            str(result),
            '<img class="type-render rounded-circle" src="https://images.example/types/4001/render" alt="Rifter">',
        )

    @patch(f"{MODULE_PATH}.type_icon_url")
    def test_should_return_url_for_icon_render(self, mock_type_icon_url):
        # Test Data
        mock_type_icon_url.return_value = "https://images.example/types/5001/icon"
        # Test Action
        result = eveonline.get_icon_render_url(type_id=5001, size=32)
        # Expected Result
        self.assertEqual(result, "https://images.example/types/5001/icon")
        mock_type_icon_url.assert_called_once_with(type_id=5001, size=32)

    @patch(f"{MODULE_PATH}.type_icon_url")
    def test_should_return_html_for_icon_render(self, mock_type_icon_url):
        # Test Data
        mock_type_icon_url.return_value = "https://images.example/types/5001/icon"
        # Test Action
        result = eveonline.get_icon_render_url(
            type_id=5001,
            size=32,
            type_name="Warp Scrambler",
            as_html=True,
        )
        # Expected Result
        self.assertEqual(
            str(result),
            '<img class="type-render rounded-circle" data-bs-tooltip="aa-killstats" src="https://images.example/types/5001/icon" title="Warp Scrambler">',
        )
