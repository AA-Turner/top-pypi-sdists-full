import os
from pathlib import Path

import numpy as np
import pytest

import ase.gui.ui as ui
from ase import Atoms
from ase.build import bulk, molecule
from ase.calculators.calculator import compare_atoms
from ase.calculators.singlepoint import SinglePointCalculator
from ase.gui.gui import GUI
from ase.gui.i18n import _
from ase.gui.quickinfo import info
from ase.gui.save import save_dialog
from ase.test.fio.test_cif import content


class GUIError(Exception):
    def __init__(self, title, text=None):
        super().__init__(title, text)


def mock_gui_error(title, text=None):
    raise GUIError(title, text)


@pytest.fixture()
def display():
    pytest.importorskip('tkinter')
    if not os.environ.get('DISPLAY'):
        raise pytest.skip('no display')


@pytest.fixture()
def gui(guifactory):
    return guifactory(None)


@pytest.fixture(autouse=True)
def no_blocking_errors_monkeypatch(monkeypatch):
    # If there's an unexpected error in one of the tests, we don't
    # want a blocking dialog to lock the whole test suite:
    for name in ['error', 'showerror', 'showwarning', 'showinfo']:
        monkeypatch.setattr(ui, name, mock_gui_error)
    # orig_ui_error = ui.error
    # ui.error = mock_gui_error
    # ui.showerror = mock_gui_error
    # ui.showwarning = mock_gui_error
    # ui.showinfo = mock_ugi_error
    # yield
    # ui.error = orig_ui_error


@pytest.fixture()
def guifactory(display):
    guis = []

    def factory(images):
        gui = GUI(images, config={})
        guis.append(gui)
        return gui

    yield factory

    for gui in guis:
        gui.exit()


@pytest.fixture()
def atoms(gui):
    atoms = bulk('Ti') * (2, 2, 2)
    gui.new_atoms(atoms)
    return atoms


@pytest.fixture()
def gui_many_images(guifactory):
    hydrogen = molecule('H2')
    hydrogen.center(5)
    images = [hydrogen.copy() for i in range(3)]
    gui = guifactory(images)
    return gui


@pytest.fixture()
def animation(guifactory):
    images = [bulk(sym) for sym in ['Cu', 'Ag', 'Au']]
    gui = guifactory(images)
    return gui


def test_about(gui):
    ui.about('name', 'version:1.1.1', 'http://webpage.org')


def test_helpwindow(gui):
    ui.helpwindow('some\n multiline\n text')


def test_arrowkey_tooltip(gui):
    gui.new_atoms(molecule('H2O'))
    gui.images.selected[0] = True
    gui.toggle_rotate_mode()
    assert not gui.arrowkey_hint.tooltip.exists
    gui.arrowkey_hint.tooltip.show()
    assert gui.arrowkey_hint.tooltip.exists


def test_nanotube(gui):
    nt = gui.nanotube_window()
    nt.apply()
    nt.element[1].value = '?'
    with pytest.raises(GUIError):
        nt.apply()

    nt.element[1].value = 'C'
    nt.ok()
    assert len(gui.images[0]) == 20


def test_nanoparticle(gui):
    n = gui.nanoparticle_window()
    n.element.symbol = 'W'  # test bcc
    n.set_structure_data()
    n.apply()
    assert len(gui.images[0]) == 57
    assert gui.images[0].get_distance(44, 45) == pytest.approx(2.737, 0.001)
    n.structure_cb.value = n.structure_names['sc']
    n.update_structure()
    n.apply()
    assert len(gui.images[0]) == 231
    assert gui.images[0].get_distance(143, 145) == pytest.approx(3.160, 0.001)
    n.structure_cb.value = n.structure_names['hcp']
    n.update_structure()
    n.apply()
    assert len(gui.images[0]) == 257
    assert gui.images[0].get_distance(4, 5) == pytest.approx(3.0, 0.001)
    assert gui.images[0].get_distance(11, 5) == pytest.approx(3.160, 0.001)
    n.element.symbol = 'Cu'  # test fcc
    n.set_structure_data()
    n.apply()
    assert len(gui.images[0]) == 675
    assert gui.images[0].get_distance(0, 1) == pytest.approx(2.553, 0.001)
    n.method_cb.value = 'wulff'
    n.update_gui_method()
    n.apply()
    assert len(gui.images[0]) == 135
    assert gui.images[0].get_distance(0, 1) == pytest.approx(2.553, 0.001)


def test_color(gui):
    a = Atoms('C10', magmoms=np.linspace(1, -1, 10))
    a.positions[:] = np.linspace(0, 9, 10)[:, None]
    a.calc = SinglePointCalculator(a, forces=a.positions)
    che = np.linspace(100, 110, 10)
    mask = [0] * 10
    mask[5] = 1
    a.set_array('corehole_energies', np.ma.array(che, mask=mask))
    gui.new_atoms(a)
    c = gui.colors_window()
    c.toggle('force')
    c.toggle('magmom')
    activebuttons = [button.active for button in c.radio.buttons]
    assert activebuttons == [1, 0, 1, 0, 0, 1, 1, 1], activebuttons
    c.toggle('corehole_energies')
    c.change_mnmx(101, 120)


def test_settings(gui):
    gui.new_atoms(molecule('H2O'))
    s = gui.settings()
    s.scale.value = 1.9
    s.scale_radii()


def test_magmom_arrows(gui):
    gui.window['toggle-show-magmoms'] = True
    gui.new_atoms(molecule('O2'))
    s = gui.settings()
    gui.magmom_vector_scale = 0.5
    s.magmom_vector_scale.value = 2.1
    s.scale_magmom_vectors()
    assert gui.magmom_vector_scale == pytest.approx(2.1)


def test_rotate(gui):
    gui.window['toggle-show-bonds'] = True
    gui.new_atoms(molecule('H2O'))
    gui.rotate_window()


def test_open_and_save(gui, testdir):
    mol = molecule('H2O')
    for j in range(3):
        mol.write('h2o.json')
    gui.open(filename='h2o.json')
    save_dialog(gui, 'h2o.cif@-1')


@pytest.mark.parametrize(
    'filename',
    [
        None,
        'output.png',
        'output.eps',
        'output.pov',
        'output.traj',
        'output.traj@0',
    ],
)
def test_export_graphics(gui, testdir, with_bulk_ti, monkeypatch, filename):
    # Monkeypatch the blocking dialog:
    monkeypatch.setattr(ui.SaveFileDialog, 'go', lambda event: filename)
    gui.save()
    if filename is not None:
        realfilename = filename.rsplit('@')[0]
        assert Path(realfilename).is_file()


def test_fracocc(gui, testdir):
    with open('./fracocc.cif', 'w') as fd:
        fd.write(content)
    gui.open(filename='fracocc.cif')


def test_povray(gui, testdir):
    mol = molecule('H2O')
    gui.new_atoms(mol)  # not gui.set_atoms(mol)
    n = gui.render_window()
    assert n.basename_widget.value == 'H2O'
    n.run_povray_widget.check.deselect()
    n.keep_files_widget.check.select()
    # can't set attribute n.run.povray_widge.value = False
    n.ok()
    ini = Path('./H2O.ini')
    pov = Path('./H2O.pov')
    assert ini.is_file()
    assert pov.is_file()

    with open(ini) as _:
        _ = _.read()
        assert 'H2O' in _
    with open(pov) as _:
        _ = _.read()
        assert 'atom' in _


@pytest.fixture()
def with_bulk_ti(gui):
    atoms = bulk('Ti') * (2, 2, 2)
    gui.new_atoms(atoms)


@pytest.fixture()
def modify(gui, with_bulk_ti):
    gui.images.selected[:4] = True
    return gui.modify_atoms()


def test_select_atoms(gui, with_bulk_ti):
    gui.select_all()
    assert all(gui.images.selected)
    gui.invert_selection()
    assert not any(gui.images.selected)


def test_modify_element(gui, modify):
    class MockElement:
        Z = 79

    modify.set_element(MockElement())
    assert all(gui.atoms.symbols[:4] == 'Au')
    assert all(gui.atoms.symbols[4:] == 'Ti')


def test_modify_tag(gui, modify):
    modify.tag.value = 17
    modify.set_tag()
    tags = gui.atoms.get_tags()
    assert all(tags[:4] == 17)
    assert all(tags[4:] == 0)


def test_modify_magmom(gui, modify):
    modify.magmom.value = 3
    modify.set_magmom()
    magmoms = gui.atoms.get_initial_magnetic_moments()
    assert magmoms[:4] == pytest.approx(3)
    assert all(magmoms[4:] == 0)


def test_repeat(gui):
    atoms = bulk('Fe')
    energy = 1.0
    atoms.calc = SinglePointCalculator(atoms, energy=energy)
    gui.new_atoms(atoms)
    repeat = gui.repeat_window()

    multiplier = [2, 3, 4]
    expected_atoms = atoms * multiplier
    natoms = np.prod(multiplier)
    for i, value in enumerate(multiplier):
        repeat.repeat[i].value = value

    repeat.change()
    assert len(gui.atoms) == natoms
    assert gui.atoms.positions == pytest.approx(expected_atoms.positions)
    assert gui.atoms.cell == pytest.approx(atoms.cell[:])  # Still old cell

    energy_ref = energy * multiplier[0] * multiplier[1] * multiplier[2]
    assert gui.images.get_energy(gui.images[0]) == pytest.approx(energy_ref)

    repeat.set_unit_cell()
    assert gui.atoms.cell[:] == pytest.approx(expected_atoms.cell[:])


def test_surface(gui):
    assert len(gui.atoms) == 0
    surf = gui.surface_window()
    surf.element.symbol = 'Au'
    surf.apply()
    assert len(gui.atoms) > 0
    assert gui.atoms.cell.rank == 2


def test_movie(animation):
    animation.movie()
    movie = animation.movie_window
    assert movie is not None

    animation.step('Home')
    assert movie.frame_number.value == 0
    animation.window.update()
    assert animation.window.moviebar.slider.get() == movie.frame_number.value

    animation.step('PageUp')
    assert movie.frame_number.value == 0

    animation.step('PageDown')
    assert movie.frame_number.value == 1

    animation.step('PageDown')
    assert movie.frame_number.value == 2
    animation.window.update()
    assert animation.window.moviebar.slider.get() == movie.frame_number.value

    last_index = len(animation.images) - 1
    animation.step('End')
    assert movie.frame_number.value == last_index

    animation.step('PageDown')
    assert movie.frame_number.value == last_index

    animation.step('PageUp')
    assert movie.frame_number.value == last_index - 1

    animation.step('PageUp')
    assert movie.frame_number.value == last_index - 2
    animation.window.update()
    assert animation.window.moviebar.slider.get() == movie.frame_number.value

    movie.play()
    movie.stop()
    movie.close()


def test_toolbar_shortcut(gui):
    assert gui.movie_window is None
    gui.window.moviebar.moviebutton.invoke()
    assert gui.movie_window is not None


def test_movie_toolbar(animation):
    assert hasattr(animation.window, 'moviebar')
    moviebar = animation.window.moviebar
    assert moviebar.slider['state'] == 'normal'
    assert moviebar.slider.get() == animation.frame

    def testagainst(val):
        # The tests will fail without an update because slider.set
        # needs a chance to do it's callback: moviebar.slidercommand
        animation.window.update()
        assert moviebar.slider.get() == val

    moviebar.click(-1, True)
    testagainst(0)

    moviebar.click(-1)
    testagainst(0)

    moviebar.click(1)
    testagainst(1)

    moviebar.click(1)
    testagainst(2)

    last_index = len(animation.images) - 1
    moviebar.click(1, True)
    testagainst(last_index)

    moviebar.click(1)
    testagainst(last_index)

    moviebar.click(-1)
    testagainst(last_index - 1)

    moviebar.click(-1)
    testagainst(last_index - 2)

    moviebar.play()
    moviebar.stop()


def test_reciprocal(gui):
    # XXX should test 1D, 2D, and it should work correctly of course
    gui.new_atoms(bulk('Au'))
    reciprocal = gui.reciprocal()
    reciprocal.terminate()
    exitcode = reciprocal.wait(timeout=5)
    reciprocal.stdout.close()
    assert exitcode != 0


def test_bad_reciprocal(gui):
    # No cell at all
    with pytest.raises(GUIError):
        gui.reciprocal()


def test_add_atoms(gui):
    dia = gui.add_atoms()
    dia.combobox.value = 'CH3CH2OH'
    assert len(gui.atoms) == 0
    dia.add()
    assert str(gui.atoms.symbols) == str(molecule('CH3CH2OH').symbols)


def test_cell_editor(gui):
    au = bulk('Au')
    gui.new_atoms(au.copy())

    dia = gui.cell_editor()

    ti = bulk('Ti')

    dia.update(ti.cell, ti.pbc)
    dia.apply_vectors()
    # Tolerance reflects the rounding (currently 7 digits)
    tol = 3e-7
    assert np.abs(gui.atoms.cell - ti.cell).max() < tol

    dia.update(ti.cell * 2, ti.pbc)
    dia.apply_magnitudes()
    assert np.abs(gui.atoms.cell - 2 * ti.cell).max() < tol

    dia.update(np.eye(3), ti.pbc)
    dia.apply_angles()
    assert abs(gui.atoms.cell.angles() - 90).max() < tol

    newpbc = [0, 1, 0]
    dia.update(np.eye(3), newpbc)
    dia.apply_pbc()
    assert (gui.atoms.pbc == newpbc).all()


def test_input_arithmetic(gui):
    """Using the cell editor to check that arithmetic in the SpinBoxes
    is parsed correctly"""
    au = bulk('Au')
    gui.new_atoms(au.copy())
    double_cell = au.cell * 2

    dia = gui.cell_editor()

    for lengths in dia.cell_grid:
        lengths[3].value = str(lengths[3].value) + '*2'
    dia.apply_magnitudes()
    assert gui.atoms.cell == pytest.approx(double_cell[:])


def test_constrain(gui, atoms):
    gui.select_all()
    dia = gui.constraints_window()

    assert len(atoms.constraints) == 0
    dia.selected()  # constrain selected
    assert len(atoms.constraints) == 1

    assert sorted(atoms.constraints[0].index) == list(range(len(atoms)))


def different_dimensionalities():
    yield molecule('H2O')
    yield Atoms('X', cell=[1, 0, 0], pbc=[1, 0, 0])
    yield Atoms('X', cell=[1, 1, 0], pbc=[1, 1, 0])
    yield bulk('Au')


@pytest.mark.parametrize('atoms', list(different_dimensionalities()))
def test_quickinfo(gui, atoms):
    gui.new_atoms(atoms)
    # (Note: String can be in any language)
    refstring = _('Single image loaded.')
    infostring = info(gui)
    assert refstring in infostring

    dia = gui.quick_info_window()
    # This is a bit weird and invasive ...
    txt = dia.things[0].text
    assert refstring in txt


def test_clipboard_copy(gui):
    atoms = molecule('CH3CH2OH')
    gui.new_atoms(atoms)
    gui.select_all()
    assert all(gui.selected_atoms().symbols == atoms.symbols)
    gui.copy_atoms_to_clipboard()
    newatoms = gui.clipboard.get_atoms()
    assert newatoms is not atoms
    assert newatoms == atoms


def test_clipboard_cut_paste(gui):
    atoms = molecule('H2O')
    gui.new_atoms(atoms.copy())
    assert len(gui.atoms) == 3
    gui.select_all()
    gui.cut_atoms_to_clipboard()
    assert len(gui.atoms) == 0
    assert atoms == gui.clipboard.get_atoms()


def test_clipboard_paste_onto_empty(gui):
    atoms = bulk('Ti')
    gui.clipboard.set_atoms(atoms)
    gui.paste_atoms_from_clipboard()
    # (The paste includes cell and pbc when existing atoms are empty)
    assert gui.atoms == atoms


def test_clipboard_paste_onto_existing(gui):
    ti = bulk('Ti')
    gui.new_atoms(ti.copy())
    assert gui.atoms == ti
    h2o = molecule('H2O')
    gui.clipboard.set_atoms(h2o)
    gui.paste_atoms_from_clipboard()
    assert gui.atoms == ti + h2o


def test_wrap(gui):
    """Test the Wrap atoms function."""
    atoms = bulk('Si')
    atoms.positions += 1234
    gui.new_atoms(atoms)
    unwrapped = atoms.get_scaled_positions(wrap=False)
    wrapped_ref = atoms.get_scaled_positions(wrap=True)

    assert (unwrapped > 1).all()
    gui.wrap_atoms()
    wrapped = gui.images[0].get_scaled_positions(wrap=False)
    assert (wrapped < 1).all()
    assert (wrapped >= 0).all()
    assert wrapped == pytest.approx(wrapped_ref)


def test_show_labels(gui):
    atoms = molecule('CH3CH2OH')
    gui.new_atoms(atoms)
    assert gui.get_labels() is None
    gui.window['show-labels'] = 3  # ugly: magical code for chemical symbols
    gui.draw()
    assert list(gui.get_labels()) == list(atoms.symbols)


@pytest.mark.parametrize(
    'text',
    [
        '',
        'invalid_atoms',
        '[1, 2, 3]',  # valid JSON but not Atoms
    ],
)
def test_clipboard_paste_invalid(gui, text):
    gui.clipboard.set_text(text)
    with pytest.raises(GUIError):
        gui.paste_atoms_from_clipboard()


def window():
    def hello(event=None):
        print('hello', event)

    menu = [
        ('Hi', [ui.MenuItem('_Hello', hello, 'Ctrl+H')]),
        ('Hell_o', [ui.MenuItem('ABC', hello, choices='ABC')]),
    ]
    win = ui.MainWindow('Test', menu=menu)

    win.add(ui.Label('Hello'))
    win.add(ui.Button('Hello', hello))

    r = ui.Rows([ui.Label(x * 7) for x in 'abcd'])
    win.add(r)
    r.add('11111\n2222\n333\n44\n5')

    def abc(x):
        print(x, r.rows)

    cb = ui.ComboBox(['Aa', 'Bb', 'Cc'], callback=abc)
    win.add(cb)

    rb = ui.RadioButtons(['A', 'B', 'C'], 'ABC', abc)
    win.add(rb)

    b = ui.CheckButton('Hello')

    def hi():
        print(b.value, rb.value, cb.value)
        del r[2]
        r.add('-------------')

    win.add([b, ui.Button('Hi', hi)])

    return win


def runcallbacks(win):
    win.things[1].callback()
    win.things[1].callback()
    win.close()


def test_callbacks(display):
    win = window()
    win.win.after_idle(runcallbacks)
    # We have created an illicit instance of tk.Tk so we must destroy it:
    win.win.destroy()


def test_atoms_editor_set_values(gui, atoms):
    editor = gui.atoms_editor()

    assert str(atoms.symbols) == 'Ti16'
    entry, apply_change = editor.edit_field(row_id='R3', column_id='#1')
    entry.delete(0, 'end')
    entry.insert(0, 'Pu')
    apply_change()

    assert str(atoms.symbols) == 'Ti3PuTi12'

    for i in range(3):
        # Edit each coordinate:
        entry, apply_change = editor.edit_field('R4', f'#{2 + i}')
        entry.delete(0, 'end')
        value = str(5.1 + i)
        entry.insert(0, value)
        apply_change()

    assert atoms.positions[4] == pytest.approx([5.1, 6.1, 7.1])


def test_atoms_editor_change_listener(gui, atoms):
    editor = gui.atoms_editor()
    entry, _ = editor.edit_field('R2', '#1')
    assert entry.get() == 'Ti'
    editor.leave_edit_mode()

    atoms = molecule('CH3CH2OH')
    gui.new_atoms(atoms)
    entry, _ = editor.edit_field('R2', '#1')
    assert entry.get() == 'O'


def test_atoms_editor_select_in_gui(gui, atoms):
    """Test that contents of editor updates when atoms change."""
    editor = gui.atoms_editor()
    assert sum(gui.images.selected) == 0
    assert len(editor.treeview.selection()) == 0

    gui.set_selected_atoms([2, 5, 6])
    selection = editor.treeview.selection()
    assert selection == ('R2', 'R5', 'R6')


def test_atoms_editor_select_in_editor(gui, atoms):
    """Test that GUI selection changes when editor selection does."""
    editor = gui.atoms_editor()
    editor.treeview.selection_set('R6', 'R7', 'R8', 'R10')
    editor.treeview.event_generate('<<TreeviewSelect>>')
    print(gui.images.selected)
    assert all(gui.images.selected[[6, 7, 8, 10]])
    assert sum(gui.images.selected) == 4


def test_atoms_history(gui):
    """Test that history can be updated, undone, redone, and rewritten"""
    gui.undo_history()
    gui.new_atoms(molecule('H2O'))
    before = gui.images[gui.frame].copy()
    gui.images.selected[0] = True
    gui.really_delete_selected_atoms()
    assert set(compare_atoms(gui.images[gui.frame], before)) == {
        'numbers',
        'positions',
    }
    gui.undo_history()
    gui.redo_history()
    gui.undo_history()
    assert not compare_atoms(gui.images[gui.frame], before)

    gui.images[gui.frame].positions *= 1.2
    gui.images.history.update_history(gui.frame)
    gui.images.history.undo_history(gui.frame)
    gui.images.history.redo_history(gui.frame)
    gui.images.history.undo_history(gui.frame)
    assert not compare_atoms(gui.images[gui.frame], before)
    gui.redo_history()

    gui.images.history.max_entries = 3
    for i in range(5):
        gui.update_history()
    assert len(gui.images.history.history_per_image[gui.frame]) == 3


def test_many_atoms_history(gui_many_images):
    """Test that history can be updated, undone, redone, and rewritten
    even while there is more than one image open in the GUI"""
    for frame in range(len(gui_many_images.images)):
        gui_many_images.set_frame(frame)
        before = gui_many_images.images[frame].copy()
        gui_many_images.images.selected[0] = True
        gui_many_images.really_delete_selected_atoms()
        assert set(compare_atoms(gui_many_images.images[frame], before)) == {
            'numbers',
            'positions',
        }
        gui_many_images.undo_history()
        gui_many_images.redo_history()
        gui_many_images.undo_history()
        assert not compare_atoms(gui_many_images.images[frame], before)


@pytest.mark.parametrize(
    'radii', [{'Cl': 5.0, 1: 3.0}, [[17, 5.0], ['H', 3.0]]]
)
def test_custom_radii(gui, radii):
    hcl = molecule('HCl')
    radius_scale = gui.images.atom_scale

    gui.new_atoms(hcl)
    gui.images.configure_radii(radii)
    radii = gui.images.get_radii(gui.atoms)
    assert radii[0] / radius_scale == pytest.approx(5.0)
    assert radii[1] / radius_scale == pytest.approx(3.0)


class MockEvent:
    def __init__(self, x, y, button, modifier=None, time=0):
        self.x = x
        self.y = y
        self.button = button
        self.modifier = modifier
        self.time = time


@pytest.fixture()
def large_gui(gui, monkeypatch):
    """GUI showing a structure above the size where the speedups apply.

    The threshold is lowered so that a modest structure (quick to draw
    in the test suite) exercises the same code paths as a large one.
    """
    monkeypatch.setattr(gui, 'LEVEL_OF_DETAIL_MIN_OBJECTS', 100)
    gui.window['toggle-show-bonds'] = True
    gui.new_atoms(bulk('Cu', cubic=True) * (4, 4, 4))

    drawn = []
    draw_indices = gui._draw_indices

    def record_draw_indices(*args):
        indices = draw_indices(*args)
        drawn.append(indices)
        return indices

    monkeypatch.setattr(gui, '_draw_indices', record_draw_indices)
    gui.drawn = drawn
    return gui


def drawn_objects(gui):
    """Atom and bond indices drawn by a fresh redraw."""
    gui.drawn.clear()
    gui.draw()
    indices = gui.drawn[-1]
    n = len(gui.atoms)
    bond_start = n + len(gui.X_cell)
    return indices[indices < n], indices[indices >= bond_start]


def test_visible_atoms():
    from ase.gui.view import View

    # Five atoms stacked in one screen cell, and one on its own in each of
    # the neighbouring cells along x and along y.
    P = np.array([[5.0, 5.0]] * 5 + [[50.0, 5.0], [5.0, 50.0]])
    z = np.array([0.0, 4.0, 1.0, 3.0, 2.0, 0.0, 0.0])
    r = np.full(7, 10.0)
    visible = View._visible_atoms(None, P, z, r, keep=3)
    assert sorted(visible) == [1, 3, 4, 5, 6]
    visible = View._visible_atoms(None, P, z, r, keep=1)
    assert sorted(visible) == [1, 5, 6]
    assert len(View._visible_atoms(None, P[:0], z[:0], r[:0])) == 0


def test_occlusion_culling(large_gui):
    gui = large_gui
    n = len(gui.atoms)
    atoms, bonds = drawn_objects(gui)
    assert 0 < len(atoms) < n
    assert len(bonds) > 0

    # Hidden atoms are still drawn if selected.
    hidden = np.setdiff1d(np.arange(n), atoms)[0]
    gui.images.selected[hidden] = True
    atoms, _ = drawn_objects(gui)
    assert hidden in atoms

    # ... and likewise if they are being moved.
    gui.images.selected[:] = False
    gui.images.selected[hidden] = True
    gui.toggle_move_mode()
    gui.images.selected[:] = False
    atoms, _ = drawn_objects(gui)
    assert hidden in atoms
    gui.toggle_move_mode()

    # Labels are drawn beside the atom, so nothing may be culled.
    gui.window['show-labels'] = 1
    atoms, _ = drawn_objects(gui)
    assert len(atoms) == n
    gui.window['show-labels'] = 0

    # Neither with the option turned off.
    gui.occlusion_culling = False
    atoms, _ = drawn_objects(gui)
    assert len(atoms) == n


def test_occlusion_culling_small_structure(gui):
    """Structures below the size threshold are drawn in full."""
    gui.new_atoms(bulk('Cu', cubic=True) * (2, 2, 2))
    gui.draw()
    assert len(gui._draw_indices(*draw_args(gui))) == len(gui.X)


def draw_args(gui):
    X = np.dot(gui.X, gui.scale * gui.axes * (1, -1, 1))
    r = gui.get_covalent_radii() * gui.scale
    return X, len(gui.atoms), r, [], None


def test_interactive_level_of_detail(large_gui):
    gui = large_gui
    atoms_static, bonds_static = drawn_objects(gui)

    gui.begin_interaction()
    assert gui.interactive
    atoms, bonds = drawn_objects(gui)
    assert len(bonds) == 0
    assert len(atoms) <= len(atoms_static)

    gui.end_interaction()
    assert not gui.interactive
    atoms, bonds = drawn_objects(gui)
    assert len(atoms) == len(atoms_static)
    assert len(bonds) == len(bonds_static)

    # With the option turned off, nothing changes while interacting.
    gui.interactive_level_of_detail = False
    gui.begin_interaction()
    atoms, bonds = drawn_objects(gui)
    assert len(bonds) == len(bonds_static)
    gui.end_interaction()


def test_interaction_settles(large_gui):
    """Full detail comes back by itself once interaction stops."""
    import time

    gui = large_gui
    gui.begin_interaction()
    gui.begin_interaction()  # re-arming must not leave a stray timer
    deadline = time.monotonic() + 5
    while gui.interactive and time.monotonic() < deadline:
        gui.window.win.update()
        time.sleep(0.01)
    assert not gui.interactive
    assert gui._settle_timer is None


def test_drag_rotate_and_release(large_gui):
    gui = large_gui
    axes = gui.axes.copy()
    gui.press(MockEvent(100, 100, gui.b3))
    gui.move(MockEvent(130, 110, gui.b3))
    assert gui.interactive
    assert not np.allclose(gui.axes, axes)
    _, bonds = drawn_objects(gui)
    assert len(bonds) == 0

    gui.release(MockEvent(130, 110, gui.b3, time=1000))
    assert not gui.interactive
    assert gui._settle_timer is None
    _, bonds = drawn_objects(gui)
    assert len(bonds) > 0


def test_rubber_band_selection(large_gui):
    from ase.gui.ui import UNCACHED_PRIMITIVES_TAG

    gui = large_gui
    canvas = gui.window.canvas
    gui.drawn.clear()
    gui.press(MockEvent(0, 0, gui.b1))
    for x in (100, 200, 300):
        gui.move(MockEvent(x, x, gui.b1))
        assert len(canvas.find_withtag(UNCACHED_PRIMITIVES_TAG)) == 1
    # Dragging the rectangle does not redraw the scene.
    assert gui.drawn == []
    assert not gui.interactive

    gui.release(MockEvent(300, 300, gui.b1, time=1000))
    assert gui.images.selected.any()


def test_large_structure_settings(large_gui):
    gui = large_gui
    settings = gui.settings()
    settings.occlusion_culling.var.set(False)
    settings.update_occlusion_culling()
    assert not gui.occlusion_culling
    settings.interactive_level_of_detail.var.set(False)
    settings.update_interactive_level_of_detail()
    assert not gui.interactive_level_of_detail
