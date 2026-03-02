document.addEventListener('DOMContentLoaded', () => {
  // This function deletes empty code blocks
  const emptyInputs = Array.from(document.querySelectorAll('.nbinput.docutils.container')).filter(
    (div) => Array.from(div.querySelectorAll('.input_area pre span')).length == 1);
  emptyInputs.forEach((elem) => elem.remove());
});
