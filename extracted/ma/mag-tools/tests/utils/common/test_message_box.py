import unittest
from unittest.mock import patch

from window.message_box import MessageBox


class TestMessageBox(unittest.TestCase):

    @patch('tkinter.messagebox.showinfo')
    def test_showinfo(self, mock_showinfo):
        mock_showinfo.return_value = 'ok'
        result = MessageBox.showinfo("Info", "This is an info message")
        self.assertEqual(result, 'ok')

    @patch('tkinter.messagebox.showwarning')
    def test_showwarning(self, mock_showwarning):
        mock_showwarning.return_value = 'ok'
        result = MessageBox.showwarning("Warning", "This is a warning message")
        self.assertEqual(result, 'ok')

    @patch('tkinter.messagebox.showerror')
    def test_showerror(self, mock_showerror):
        mock_showerror.return_value = 'ok'
        result = MessageBox.showerror("Error", "This is an error message")
        self.assertEqual(result, 'ok')

    @patch('tkinter.messagebox.askquestion')
    def test_askquestion(self, mock_askquestion):
        mock_askquestion.return_value = 'yes'
        result = MessageBox.askquestion("Question", "Is this a question?")
        self.assertEqual(result, 'yes')

    @patch('tkinter.messagebox.askokcancel')
    def test_askokcancel(self, mock_askokcancel):
        mock_askokcancel.return_value = True
        result = MessageBox.askokcancel("OK Cancel", "Do you want to proceed?")
        self.assertTrue(result)

    @patch('tkinter.messagebox.askyesno')
    def test_askyesno(self, mock_askyesno):
        mock_askyesno.return_value = True
        result = MessageBox.askyesno("Yes No", "Do you agree?")
        self.assertTrue(result)

    @patch('tkinter.messagebox.askyesnocancel')
    def test_askyesnocancel(self, mock_askyesnocancel):
        mock_askyesnocancel.return_value = True
        result = MessageBox.askyesnocancel("Yes No Cancel", "Do you want to continue?")
        self.assertTrue(result)

    @patch('tkinter.messagebox.askretrycancel')
    def test_askretrycancel(self, mock_askretrycancel):
        mock_askretrycancel.return_value = True
        result = MessageBox.askretrycancel("Retry Cancel", "Do you want to retry?")
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
