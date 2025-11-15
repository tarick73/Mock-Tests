import unittest
from unittest.mock import patch, MagicMock, mock_open

from pokemon_service import PokemonService
from pokemon_name_translator import PokemonNameTranslator
from pokemon_report import PokemonReport


class TestPokemonService(unittest.TestCase):
    @patch("pokemon_service.requests.get")
    def test_get_pokemon_info_success(self, mock_get):
        fake_response = MagicMock()
        fake_response.status_code = 200
        fake_response.json.return_value = {"name": "pikachu"}
        mock_get.return_value = fake_response

        service = PokemonService()
        result = service.get_pokemon_info("pikachu")

        self.assertEqual(result, {"name": "pikachu"})




class TestPokemonNameTranslator(unittest.TestCase):
    @patch("pokemon_name_translator.translate.TranslationServiceClient")
    def test_translate_returns_text(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client

        fake_translation = MagicMock()
        fake_translation.translated_text = "Пикачу (FR)"

        fake_response = MagicMock()
        fake_response.translations = [fake_translation]
        mock_client.translate_text.return_value = fake_response

        translator = PokemonNameTranslator()
        result = translator.translate("pikachu", target_language="fr")

        mock_client.translate_text.assert_called_once()
        self.assertEqual(result, "Пикачу (FR)")


class TestPokemonReport(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    def test_create_html_report_writes_file(self, mock_file):
        report = PokemonReport()
        pokemon_info = {
            "name": "pikachu",
            "height": 4,
            "weight": 60,
            "abilities": [
                {"ability": {"name": "static"}},
                {"ability": {"name": "lightning"}},
            ],
        }
        translated_name = "Пикачу"

        path = report.create_html_report(pokemon_info, translated_name)

        self.assertEqual(path, "report_template.html")

        mock_file.assert_called_once_with("report_template.html", "w", encoding="utf-8")

    @patch("pokemon_report.pdfkit.from_file")
    @patch.object(PokemonReport, "create_html_report", return_value="report_template.html")
    def test_generate_report_calls_pdfkit(self, mock_create_html, mock_from_file):
        report = PokemonReport()
        pokemon_info = {"name": "pikachu", "height": 4, "weight": 60, "abilities": []}
        translated_name = "Пикачу"
        output_pdf = "pokemon_report.pdf"

        report.generate_report(pokemon_info, translated_name, output_pdf)

        mock_create_html.assert_called_once_with(pokemon_info, translated_name)
        mock_from_file.assert_called_once()



if __name__ == "__main__":
    unittest.main()
