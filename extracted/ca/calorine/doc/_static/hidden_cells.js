document.addEventListener('DOMContentLoaded', () => {

  // Functions to create show and hide buttons

  const addShowCode = (div) => {
    const button = document.createElement('div');
    button.classList.add('my-nbsphinx-showbutton');
    button.classList.add('highlight');
    button.innerHTML = ' >>> Show code <<<';
    button.onclick = () => {div.classList.remove('my-nbsphinx-folded')};
    div.insertAdjacentElement('afterbegin', button);
  };

  const addHideCode = (div) => {
    const button = document.createElement('div');
    button.classList.add('my-nbsphinx-hidebutton');
    button.classList.add('highlight');
    button.innerHTML = ' >>> Hide code <<<';
    button.onclick = () => {div.classList.add('my-nbsphinx-folded')};
    div.insertAdjacentElement('afterbegin', button);

		// Hide code by default
    div.classList.add('my-nbsphinx-folded');
  };

  const addShowOutput = (div) => {
    const button = document.createElement('div');
    button.classList.add('my-nbsphinx-showbutton');
    button.innerHTML = ' >>> Show output <<<';
    button.onclick = () => {div.classList.remove('my-nbsphinx-folded')};
    div.insertAdjacentElement('afterbegin', button);
  };

  const addHideOutput = (div) => {
    const button = document.createElement('div');
    button.classList.add('my-nbsphinx-hidebutton');
    button.innerHTML = ' >>> Hide output <<<';
    button.onclick = () => {div.classList.add('my-nbsphinx-folded')};
    div.insertAdjacentElement('afterbegin', button);

		// Hide output by default
    div.classList.add('my-nbsphinx-folded');
  };

	// Find inputs in the HTML immediately following an element of class 'hide-next-input'
	const hideCodeDivs = document.querySelectorAll('.hide-next-input + .nbinput.container');
	// These elements should have collpsed inputs
  hideCodeDivs.forEach(addShowCode);
  hideCodeDivs.forEach(addHideCode);

	// Find outputs in the HTML immediately following an input immediately following an element of class 'hide-next-output'
	const hideOutputDivs = document.querySelectorAll('.hide-next-output + .nbinput.container + .nboutput.container');
	// These elements should have collpsed outputs
  hideOutputDivs.forEach(addShowOutput);
  hideOutputDivs.forEach(addHideOutput);
});
