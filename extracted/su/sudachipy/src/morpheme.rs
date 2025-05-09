/*
 *  Copyright (c) 2021-2024 Works Applications Co., Ltd.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *   Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

use std::fmt::Write;
use std::ops::Deref;
use std::sync::Arc;

use pyo3::exceptions::PyIndexError;
use pyo3::ffi::c_str;
use pyo3::prelude::*;
use pyo3::types::{PyList, PyString, PyTuple, PyType};

use sudachi::prelude::{Morpheme, MorphemeList};

use crate::dictionary::{extract_mode, PyDicData, PyDictionary};
use crate::errors;
use crate::projection::{MorphemeProjection, PyProjector};
use crate::word_info::PyWordInfo;

pub(crate) type PyMorphemeList = MorphemeList<Arc<PyDicData>>;

/// A list of morphemes.
///
/// An object can not be instantiated manually.
/// Use Tokenizer.tokenize("") to create an empty morpheme list.
#[pyclass(module = "sudachipy.morphemelist", name = "MorphemeList")]
pub struct PyMorphemeListWrapper {
    /// use `internal()` function instead
    inner: PyMorphemeList,
    projection: PyProjector,
}

// PyMorphemeListWrapper is used only when GIL is active,
// all associated functions take GIL token as a parameter
unsafe impl Sync for PyMorphemeListWrapper {}
unsafe impl Send for PyMorphemeListWrapper {}

impl PyMorphemeListWrapper {
    pub(crate) fn new(dict: Arc<PyDicData>) -> Self {
        let proj = dict.projection.clone();
        Self {
            inner: PyMorphemeList::empty(dict),
            projection: proj,
        }
    }

    pub(crate) fn from_components(list: PyMorphemeList, projection: PyProjector) -> Self {
        Self {
            inner: list,
            projection,
        }
    }

    pub(crate) fn projection(&self) -> Option<&dyn MorphemeProjection> {
        match &self.projection {
            None => None,
            Some(p) => Some(p.as_ref()),
        }
    }

    /// Borrow internals mutable. GIL token proves access.
    pub(crate) fn internal_mut(&mut self, _py: Python) -> &mut PyMorphemeList {
        &mut self.inner
    }

    /// Borrow internals immutable. GIL token proves access.
    #[inline]
    pub(crate) fn internal(&self, _py: Python) -> &PyMorphemeList {
        &self.inner
    }

    /// Create a copy with empty list of Nodes. GIL token proves access.
    pub(crate) fn empty_clone(&self, _py: Python) -> Self {
        Self {
            inner: self.inner.empty_clone(),
            projection: self.projection.clone(),
        }
    }
}

#[pymethods]
impl PyMorphemeListWrapper {
    /// Returns an empty morpheme list with dictionary.
    ///
    /// .. deprecated:: 0.6.0
    ///     Use Tokenizer.tokenize("") if you need.
    #[classmethod]
    #[pyo3(text_signature = "(dict: Dictionary) -> MorphemeList")]
    fn empty(_cls: &Bound<PyType>, py: Python, dict: &PyDictionary) -> PyResult<Self> {
        errors::warn_deprecation(
            py,
            c_str!("Use Tokenizer.tokenize(\"\") if you need an empty MorphemeList."),
        )?;

        let cloned = dict.dictionary.as_ref().unwrap().clone();
        let proj = cloned.projection.clone();
        Ok(Self {
            inner: PyMorphemeList::empty(cloned),
            projection: proj,
        })
    }

    /// Returns the total cost of the path.
    #[pyo3(text_signature = "(self, /) -> int")]
    fn get_internal_cost(&self, py: Python) -> i32 {
        self.internal(py).get_internal_cost()
    }

    /// Returns the number of morpheme in this list.
    #[pyo3(text_signature = "(self, /) -> int")]
    fn size(&self, py: Python) -> usize {
        self.internal(py).len()
    }

    fn __len__(&self, py: Python) -> usize {
        self.size(py)
    }

    fn __getitem__(slf: Bound<PyMorphemeListWrapper>, mut idx: isize) -> PyResult<PyMorpheme> {
        let list = slf.borrow();
        let py = slf.py();
        let len = list.size(py) as isize;

        if idx < 0 {
            // negative indexing
            idx += len;
        }

        if idx < 0 || len <= idx {
            return Err(PyIndexError::new_err(format!(
                "MorphemeList index out of range: the len is {} but the index is {}",
                list.size(py),
                idx
            )));
        }

        let py_list: Py<PyMorphemeListWrapper> = slf.into();

        Ok(PyMorpheme {
            list: py_list,
            index: idx as usize,
        })
    }

    fn __str__<'py>(&'py self, py: Python<'py>) -> Bound<'py, PyString> {
        // do a simple tokenization __str__
        let list = self.internal(py);
        let mut result = String::with_capacity(list.surface().len() * 2);
        let nmorphs = list.len();
        for (i, m) in list.iter().enumerate() {
            result.push_str(m.surface().deref());
            if i + 1 != nmorphs {
                result.push(' ');
            }
        }
        PyString::new(py, result.as_str())
    }

    fn __repr__(slf: Py<PyMorphemeListWrapper>, py: Python) -> PyResult<Bound<PyString>> {
        let self_ref = slf.borrow(py);
        let list = self_ref.internal(py);
        let mut result = String::with_capacity(list.surface().len() * 10);
        result.push_str("<MorphemeList[\n");
        let nmorphs = list.len();
        for i in 0..nmorphs {
            result.push_str("  ");
            let pymorph = PyMorpheme {
                list: slf.clone_ref(py),
                index: i,
            };
            errors::wrap_ctx(pymorph.write_repr(py, &mut result), "format failed")?;
            result.push_str(",\n");
        }
        result.push_str("]>");
        Ok(PyString::new(py, result.as_str()))
    }

    fn __iter__(slf: Py<Self>) -> PyMorphemeIter {
        PyMorphemeIter {
            list: slf,
            index: 0,
        }
    }

    fn __bool__(&self, py: Python) -> bool {
        !self.internal(py).is_empty()
    }
}

/// An iterator over the MorphemeList.
#[pyclass(module = "sudachipy.morphemelist", name = "MorphemeIter")]
pub struct PyMorphemeIter {
    list: Py<PyMorphemeListWrapper>,
    index: usize,
}

#[pymethods]
impl PyMorphemeIter {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }

    fn __next__(&mut self, py: Python) -> Option<PyMorpheme> {
        if self.index >= self.list.borrow(py).size(py) {
            return None;
        }

        let morpheme = PyMorpheme {
            list: self.list.clone_ref(py),
            index: self.index,
        };

        self.index += 1;
        Some(morpheme)
    }
}

/// It is a syntax sugar for accessing Morpheme reference
/// Without it binding implementations become much less readable
struct MorphemeRef<'py> {
    #[allow(unused)] // need to keep this around for correct reference count
    list: PyRef<'py, PyMorphemeListWrapper>,
    morph: Morpheme<'py, Arc<PyDicData>>,
}

impl<'py> Deref for MorphemeRef<'py> {
    type Target = Morpheme<'py, Arc<PyDicData>>;

    fn deref(&self) -> &Self::Target {
        &self.morph
    }
}

/// A morpheme (basic semantic unit of language).
#[pyclass(module = "sudachipy.morpheme", name = "Morpheme", frozen)]
pub struct PyMorpheme {
    list: Py<PyMorphemeListWrapper>,
    index: usize,
}

impl PyMorpheme {
    fn list<'py>(&'py self, py: Python<'py>) -> PyRef<'py, PyMorphemeListWrapper> {
        self.list.borrow(py)
    }

    fn morph<'py>(&'py self, py: Python<'py>) -> MorphemeRef<'py> {
        let list = self.list(py);
        // workaround for self-referential structs
        let morph = unsafe { std::mem::transmute(list.internal(py).get(self.index)) };
        MorphemeRef { list, morph }
    }

    fn write_repr<'py, W: Write>(&'py self, py: Python<'py>, out: &mut W) -> std::fmt::Result {
        // per https://github.com/WorksApplications/SudachiPy/pull/166#issuecomment-932043063
        let mrp = self.morph(py);
        let surf = mrp.surface();
        write!(
            out,
            "<Morpheme({}, {}:{}, {})>",
            surf.deref(),
            mrp.begin_c(),
            mrp.end_c(),
            mrp.word_id()
        )
    }
}

#[pymethods]
impl PyMorpheme {
    /// Returns the begin index of this in the input text.
    #[pyo3(text_signature = "(self, /) -> int")]
    fn begin(&self, py: Python) -> usize {
        // call codepoint version
        self.morph(py).begin_c()
    }

    /// Returns the end index of this in the input text.
    #[pyo3(text_signature = "(self, /) -> int")]
    fn end(&self, py: Python) -> usize {
        // call codepoint version
        self.morph(py).end_c()
    }

    /// Returns the substring of input text corresponding to the morpheme, or a projection if one is configured.
    ///
    /// See `Config.projection`.
    #[pyo3(text_signature = "(self, /) -> str")]
    fn surface<'py>(&'py self, py: Python<'py>) -> Bound<'py, PyString> {
        let list = self.list(py);
        let morph = self.morph(py);
        match list.projection() {
            None => PyString::new(py, morph.surface().deref()),
            Some(proj) => proj.project(morph.deref(), py),
        }
    }

    /// Returns the substring of input text corresponding to the morpheme regardless the configured projection.
    ///
    /// See `Config.projection`.
    #[pyo3(text_signature = "(self, /) -> str")]
    fn raw_surface<'py>(&'py self, py: Python<'py>) -> Bound<'py, PyString> {
        PyString::new(py, self.morph(py).surface().deref())
    }

    /// Returns the part of speech as a six-element tuple.
    /// Tuple elements are four POS levels, conjugation type and conjugation form.
    #[pyo3(text_signature = "(self, /) -> tuple[str, str, str, str, str, str]")]
    fn part_of_speech<'py>(&'py self, py: Python<'py>) -> Py<PyTuple> {
        let pos_id = self.part_of_speech_id(py);
        self.list(py)
            .internal(py)
            .dict()
            .pos_of(pos_id)
            .clone_ref(py)
    }

    /// Returns the id of the part of speech in the dictionary.
    #[pyo3(text_signature = "(self, /) -> int")]
    pub fn part_of_speech_id(&self, py: Python) -> u16 {
        self.morph(py).part_of_speech_id()
    }

    /// Returns the dictionary form.
    #[pyo3(text_signature = "(self, /) -> str")]
    fn dictionary_form<'py>(&'py self, py: Python<'py>) -> PyResult<Bound<PyString>> {
        Ok(self
            .morph(py)
            .get_word_info()
            .dictionary_form()
            .into_pyobject(py)?)
    }

    /// Returns the normalized form.
    #[pyo3(text_signature = "(self, /) -> str")]
    fn normalized_form<'py>(&'py self, py: Python<'py>) -> PyResult<Bound<PyString>> {
        Ok(self
            .morph(py)
            .get_word_info()
            .normalized_form()
            .into_pyobject(py)?)
    }

    /// Returns the reading form.
    #[pyo3(text_signature = "(self, /) -> str")]
    fn reading_form<'py>(&'py self, py: Python<'py>) -> PyResult<Bound<PyString>> {
        Ok(self
            .morph(py)
            .get_word_info()
            .reading_form()
            .into_pyobject(py)?)
    }

    /// Returns sub-morphemes in the provided split mode.
    ///
    /// :param mode: mode of new split.
    /// :param out: write results to this MorhpemeList instead of creating new one.
    ///     See https://worksapplications.github.io/sudachi.rs/python/topics/out_param.html for
    ///     more information on output parameters.
    ///     Returned MorphemeList will be invalidated if this MorphemeList is used as an output parameter.
    /// :param add_single: return lists with the current morpheme if the split hasn't produced any elements.
    ///     When False is passed, empty lists are returned instead.
    ///
    /// :type mode: SplitMode | None
    /// :type out: MorphemeList | None
    /// :type add_single: bool
    #[pyo3(
        signature = (mode, out=None, add_single=false),
        text_signature = "(self, /, mode, out=None, add_single=False) -> MorphemeList",
    )]
    fn split<'py>(
        &'py self,
        py: Python<'py>,
        mode: &Bound<'py, PyAny>,
        out: Option<Bound<'py, PyMorphemeListWrapper>>,
        add_single: Option<bool>,
    ) -> PyResult<Bound<'py, PyMorphemeListWrapper>> {
        let list = self.list(py);

        let mode = extract_mode(mode)?;

        let out_cell = match out {
            None => {
                let list = list.empty_clone(py);
                Bound::new(py, list)?
            }
            Some(r) => r,
        };

        let mut borrow = out_cell.try_borrow_mut();
        let out_ref = match borrow {
            Ok(ref mut v) => v.internal_mut(py),
            Err(_) => return errors::wrap(Err("out was used twice at the same time")),
        };

        out_ref.clear();
        let splitted = errors::wrap_ctx(
            list.internal(py).split_into(mode, self.index, out_ref),
            "Error while splitting morpheme",
        )?;

        if add_single.unwrap_or(true) && !splitted {
            list.internal(py)
                .copy_slice(self.index, self.index + 1, out_ref);
        }

        Ok(out_cell)
    }

    /// Returns whether if this is out of vocabulary word.
    #[pyo3(text_signature = "(self, /) -> bool")]
    fn is_oov(&self, py: Python) -> bool {
        self.morph(py).is_oov()
    }

    /// Returns word id of this word in the dictionary.
    #[pyo3(text_signature = "(self, /) -> int")]
    fn word_id(&self, py: Python) -> u32 {
        self.morph(py).word_id().as_raw()
    }

    /// Returns the dictionary id which this word belongs.
    #[pyo3(text_signature = "(self, /) -> int")]
    fn dictionary_id(&self, py: Python) -> i32 {
        let word_id = self.morph(py).word_id();
        if word_id.is_oov() {
            -1
        } else {
            word_id.dic() as i32
        }
    }

    /// Returns the list of synonym group ids.
    #[pyo3(text_signature = "(self, /) -> List[int]")]
    fn synonym_group_ids<'py>(&'py self, py: Python<'py>) -> PyResult<Bound<PyList>> {
        let mref = self.morph(py);
        let ids = mref.get_word_info().synonym_group_ids();
        PyList::new(py, ids)
    }

    /// Returns the word info.
    ///
    /// ..deprecated:: v0.6.0
    ///    Users should not touch the raw WordInfo.
    #[pyo3(text_signature = "(self, /) -> WordInfo")]
    fn get_word_info(&self, py: Python) -> PyResult<PyWordInfo> {
        errors::warn_deprecation(py, c_str!("Users should not touch the raw WordInfo."))?;
        Ok(self.morph(py).get_word_info().clone().into())
    }

    /// Returns morpheme length in codepoints.
    pub fn __len__(&self, py: Python) -> usize {
        let m = self.morph(py);
        m.end_c() - m.begin_c()
    }

    pub fn __str__<'py>(&'py self, py: Python<'py>) -> Bound<'py, PyString> {
        self.surface(py)
    }

    pub fn __repr__<'py>(&'py self, py: Python<'py>) -> PyResult<String> {
        let mut result = String::new();
        errors::wrap_ctx(self.write_repr(py, &mut result), "failed to format repr")?;
        Ok(result)
    }
}
