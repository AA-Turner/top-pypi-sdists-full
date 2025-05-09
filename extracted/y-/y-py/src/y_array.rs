use std::convert::{TryFrom, TryInto};

use crate::json_builder::JsonBuilder;
use crate::shared_types::{
    CompatiblePyType, DeepSubscription, DefaultPyErr, PreliminaryObservationException,
    ShallowSubscription, SubId,
};
use crate::type_conversions::events_into_py;
use crate::y_transaction::YTransaction;

use super::shared_types::SharedType;
use crate::type_conversions::ToPython;
use lib0::any::Any;
use pyo3::exceptions::PyIndexError;

use crate::type_conversions::PyObjectWrapper;
use pyo3::prelude::*;
use pyo3::types::{PyList, PySlice, PySliceIndices};
use yrs::types::array::ArrayEvent;
use yrs::types::DeepObservable;
use yrs::{Array, SubscriptionId, Transaction};

/// A collection used to store data in an indexed sequence structure. This type is internally
/// implemented as a double linked list, which may squash values inserted directly one after another
/// into single list node upon transaction commit.
///
/// Reading a root-level type as an YArray means treating its sequence components as a list, where
/// every countable element becomes an individual entity:
///
/// - JSON-like primitives (booleans, numbers, strings, JSON maps, arrays etc.) are counted
///   individually.
/// - Text chunks inserted by [Text] data structure: each character becomes an element of an
///   array.
/// - Embedded and binary values: they count as a single element even though they correspond of
///   multiple bytes.
///
/// Like all Yrs shared data types, YArray is resistant to the problem of interleaving (situation
/// when elements inserted one after another may interleave with other peers concurrent inserts
/// after merging all updates together). In case of Yrs conflict resolution is solved by using
/// unique document id to determine correct and consistent ordering.
#[pyclass(unsendable)]
pub struct YArray(pub SharedType<Array, Vec<PyObject>>);

impl From<Array> for YArray {
    fn from(v: Array) -> Self {
        YArray(SharedType::new(v))
    }
}

#[pymethods]
impl YArray {
    /// Creates a new preliminary instance of a `YArray` shared data type, with its state
    /// initialized to provided parameter.
    ///
    /// Preliminary instances can be nested into other shared data types such as `YArray` and `YMap`.
    /// Once a preliminary instance has been inserted this way, it becomes integrated into Ypy
    /// document store and cannot be nested again: attempt to do so will result in an exception.
    #[new]
    pub fn new(init: Option<PyObject>) -> PyResult<Self> {
        let elements = init.map(Self::py_iter).unwrap_or(Ok(Vec::default()));
        elements.map(|el_array| YArray(SharedType::prelim(el_array)))
    }

    /// Returns true if this is a preliminary instance of `YArray`.
    ///
    /// Preliminary instances can be nested into other shared data types such as `YArray` and `YMap`.
    /// Once a preliminary instance has been inserted this way, it becomes integrated into Ypy
    /// document store and cannot be nested again: attempt to do so will result in an exception.
    #[getter]
    pub fn prelim(&self) -> bool {
        match &self.0 {
            SharedType::Prelim(_) => true,
            _ => false,
        }
    }

    /// Returns a number of elements stored within this instance of `YArray`.
    pub fn __len__(&self) -> usize {
        match &self.0 {
            SharedType::Integrated(v) => v.len() as usize,
            SharedType::Prelim(v) => v.len() as usize,
        }
    }

    pub fn __str__(&self) -> String {
        match &self.0 {
            SharedType::Integrated(y_array) => {
                let any = y_array.to_json();
                let py_values = Python::with_gil(|py| any.into_py(py));
                py_values.to_string()
            }
            SharedType::Prelim(py_contents) => {
                let py_values = Python::with_gil(|py| py_contents.clone().into_py(py));
                py_values.to_string()
            }
        }
    }

    pub fn __repr__(&self) -> String {
        format!("YArray({})", self.__str__())
    }

    /// Converts an underlying contents of this `YArray` instance into their JSON representation.
    pub fn to_json(&self) -> PyResult<String> {
        let mut json_builder = JsonBuilder::new();
        match &self.0 {
            SharedType::Integrated(array) => json_builder.append_json(&array.to_json())?,
            SharedType::Prelim(py_vec) => json_builder.append_json(py_vec)?,
        }
        Ok(json_builder.into())
    }
    /// Adds a single item to the provided index in the array.
    pub fn insert(&mut self, txn: &mut YTransaction, index: u32, item: PyObject) -> PyResult<()> {
        match &mut self.0 {
            SharedType::Integrated(array) if array.len() >= index => {
                array.insert(txn, index, PyObjectWrapper(item));
                Ok(())
            }
            SharedType::Prelim(vec) if vec.len() >= index as usize => {
                Ok(vec.insert(index as usize, item))
            }
            _ => Err(PyIndexError::default_message()),
        }
    }

    /// Inserts a given range of `items` into this `YArray` instance, starting at given `index`.
    pub fn insert_range(
        &mut self,
        txn: &mut YTransaction,
        index: u32,
        items: PyObject,
    ) -> PyResult<()> {
        let items = Self::py_iter(items)?;
        match &mut self.0 {
            SharedType::Integrated(array) if array.len() >= index => {
                Self::insert_multiple_at(array, txn, index, items)?;
                Ok(())
            }
            SharedType::Prelim(vec) if vec.len() >= index as usize => {
                let mut j = index;
                for el in items {
                    vec.insert(j as usize, el);
                    j += 1;
                }
                Ok(())
            }
            _ => Err(PyIndexError::default_message()),
        }
    }

    /// Appends a range of `items` at the end of this `YArray` instance.
    pub fn extend(&mut self, txn: &mut YTransaction, items: PyObject) -> PyResult<()> {
        let index = self.__len__() as u32;
        self.insert_range(txn, index, items)
    }
    /// Adds a single item to the end of the array
    pub fn append(&mut self, txn: &mut YTransaction, item: PyObject) {
        match &mut self.0 {
            SharedType::Integrated(array) => array.push_back(txn, PyObjectWrapper(item)),
            SharedType::Prelim(vec) => vec.push(item),
        }
    }
    /// Removes the element that the given index from the list.
    pub fn delete(&mut self, txn: &mut YTransaction, index: u32) -> PyResult<()> {
        match &mut self.0 {
            SharedType::Integrated(v) if index < v.len() => Ok(v.remove(txn, index)),
            SharedType::Prelim(v) if index < v.len() as u32 => {
                v.remove(index as usize);
                Ok(())
            }
            _ => Err(PyIndexError::default_message()),
        }
    }

    /// Deletes a range of items of given `length` from current `YArray` instance,
    /// starting from given `index`.
    pub fn delete_range(&mut self, txn: &mut YTransaction, index: u32, length: u32) {
        match &mut self.0 {
            SharedType::Integrated(v) => v.remove_range(txn, index, length),
            SharedType::Prelim(v) => {
                v.drain((index as usize)..(index + length) as usize);
            }
        }
    }

    /// Moves the element from the index source to target.
    pub fn move_to(&mut self, txn: &mut YTransaction, source: u32, target: u32) -> PyResult<()> {
        match &mut self.0 {
            SharedType::Integrated(v) => {
                v.move_to(txn, source, target);
                Ok(())
            }
            SharedType::Prelim(_) if source < 0 as u32 || target < 0 as u32 => {
                Err(PyIndexError::default_message())
            }
            SharedType::Prelim(v) if source < v.len() as u32 && target < v.len() as u32 => {
                if source < target {
                    let el = v.remove(source as usize);
                    v.insert((target - 1) as usize, el);
                } else if source > target {
                    let el = v.remove(source as usize);
                    v.insert(target as usize, el);
                }
                Ok(())
            }
            _ => Err(PyIndexError::default_message()),
        }
    }

    /// Moves all elements found within `start`..`end` indexes range (both side inclusive) into
    /// new position pointed by `target` index. All elements inserted concurrently by other peers
    /// inside of moved range will be moved as well after synchronization (although it make take
    /// more than one sync roundtrip to achieve convergence).
    ///
    /// `assoc_start`/`assoc_end` flags are used to mark if ranges should include elements that
    /// might have been inserted concurrently at the edges of the range definition.
    ///
    /// Example:
    /// ```
    /// use yrs::Doc;
    /// let doc = Doc::new();
    /// let array = doc.transact().get_array("array");
    /// array.insert_range(&mut doc.transact(), 0, [1,2,3,4]);
    /// // move elements 2 and 3 after the 4
    /// array.move_range_to(&mut doc.transact(), 1, 2, 4);
    /// ```
    pub fn move_range_to(
        &mut self,
        txn: &mut YTransaction,
        start: u32,
        end: u32,
        target: u32,
    ) -> PyResult<()> {
        match &mut self.0 {
            SharedType::Integrated(v) => {
                v.move_range_to(txn, start, true, end, false, target);
                Ok(())
            }

            // y-rs does nothing if end < start
            // SharedType::Prelim(_) if end < start => Err(PyIndexError::default_message()),
            SharedType::Prelim(_) if start < 0 as u32 || end < 0 as u32 || target < 0 as u32 => {
                Err(PyIndexError::default_message())
            }
            SharedType::Prelim(v)
                if start > v.len() as u32 || end > v.len() as u32 || target > v.len() as u32 =>
            {
                Err(PyIndexError::default_message())
            }

            // It doesn't make sense to move a range into the same range (it's basically a no-op).
            SharedType::Prelim(_) if target >= start && target <= end => Ok(()),

            SharedType::Prelim(v) => {
                let mut i: usize = 0;
                let mut n: usize = (end - start + 1) as usize;
                let backwards = target > end;

                while n > 0 {
                    let item = v.remove(start as usize + i);
                    if backwards {
                        v.insert(target as usize - 1, item);
                    } else {
                        v.insert(target as usize + i, item);
                        i += 1;
                    }
                    n -= 1;
                }
                Ok(())
            }
        }
    }

    pub fn __getitem__(&self, index: Index) -> PyResult<PyObject> {
        // Apply index to the Array type
        match index {
            Index::Int(index) => self.get_element(self.normalize_index(index)),
            Index::Slice(slice) => self.get_range(slice),
        }
    }

    /// Returns an iterator that can be used to traverse over the values stored withing this
    /// instance of `YArray`.
    ///
    /// Example:
    ///
    /// ```python
    /// from y_py import YDoc
    ///
    /// # document on machine A
    /// doc = YDoc()
    /// array = doc.get_array('name')
    /// for item in array:
    ///     print(item)
    ///     
    /// ```
    pub fn __iter__(&self) -> PyObject {
        Python::with_gil(|py| {
            let list: PyObject = match &self.0 {
                SharedType::Integrated(arr) => arr.to_json().into_py(py),
                SharedType::Prelim(arr) => arr.clone().into_py(py),
            };
            let any = list.as_ref(py);
            any.iter().unwrap().into_py(py)
        })
    }

    /// Subscribes to all operations happening over this instance of `YArray`. All changes are
    /// batched and eventually triggered during transaction commit phase.
    /// Returns a `SubscriptionId` which can be used to cancel the callback with `unobserve`.
    pub fn observe(&mut self, f: PyObject) -> PyResult<ShallowSubscription> {
        match &mut self.0 {
            SharedType::Integrated(array) => {
                let sub: SubscriptionId = array
                    .observe(move |txn, e| {
                        Python::with_gil(|py| {
                            let event = YArrayEvent::new(e, txn);
                            if let Err(err) = f.call1(py, (event,)) {
                                err.restore(py)
                            }
                        })
                    })
                    .into();
                Ok(ShallowSubscription(sub))
            }
            SharedType::Prelim(_) => Err(PreliminaryObservationException::default_message()),
        }
    }
    /// Observes YArray events and events of all child elements.
    pub fn observe_deep(&mut self, f: PyObject) -> PyResult<DeepSubscription> {
        match &mut self.0 {
            SharedType::Integrated(array) => {
                let sub: SubscriptionId = array
                    .observe_deep(move |txn, events| {
                        Python::with_gil(|py| {
                            let events = events_into_py(txn, events);
                            if let Err(err) = f.call1(py, (events,)) {
                                err.restore(py)
                            }
                        })
                    })
                    .into();
                Ok(DeepSubscription(sub))
            }
            SharedType::Prelim(_) => Err(PreliminaryObservationException::default_message()),
        }
    }

    /// Cancels the callback of an observer using the Subscription ID returned from the `observe` method.
    pub fn unobserve(&mut self, subscription_id: SubId) -> PyResult<()> {
        match &mut self.0 {
            SharedType::Integrated(arr) => Ok(match subscription_id {
                SubId::Shallow(ShallowSubscription(id)) => arr.unobserve(id),
                SubId::Deep(DeepSubscription(id)) => arr.unobserve_deep(id),
            }),
            SharedType::Prelim(_) => Err(PreliminaryObservationException::default_message()),
        }
    }
}

impl YArray {
    /// Gets a single element from a YArray.
    fn get_element(&self, index: u32) -> PyResult<PyObject> {
        match &self.0 {
            SharedType::Integrated(v) => {
                if let Some(value) = v.get(index as u32) {
                    Ok(Python::with_gil(|py| value.into_py(py)))
                } else {
                    Err(PyIndexError::default_message())
                }
            }
            SharedType::Prelim(v) => {
                if let Some(value) = v.get(index as usize) {
                    Ok(value.clone())
                } else {
                    Err(PyIndexError::default_message())
                }
            }
        }
    }

    /// Creates a new YArray from a range of values specified in a PySlice
    fn get_range(&self, slice: &PySlice) -> PyResult<PyObject> {
        let PySliceIndices {
            start, stop, step, ..
        } = slice.indices(self.__len__().try_into().unwrap()).unwrap();
        match &self.0 {
            SharedType::Integrated(arr) => Python::with_gil(|py| {
                if step < 0 {
                    let step = step.abs() as usize;
                    let (start, stop) = ((stop + 1) as usize, (start + 1) as usize);
                    let values: Vec<PyObject> = arr
                        .iter()
                        .enumerate()
                        .skip(start)
                        .step_by(step)
                        .take_while(|(i, _)| i < &stop)
                        .map(|(_, el)| el.into_py(py))
                        .collect();
                    let values: Vec<PyObject> = values.into_iter().rev().collect();
                    Ok(values.into_py(py))
                } else {
                    let (start, stop, step) = (start as usize, stop as usize, step as usize);
                    let values: Vec<PyObject> = arr
                        .iter()
                        .enumerate()
                        .skip(start)
                        .step_by(step)
                        .take_while(|(i, _)| i < &stop)
                        .map(|(_, el)| el.into_py(py))
                        .collect();
                    Ok(values.into_py(py))
                }
            }),
            SharedType::Prelim(arr) => Python::with_gil(|py| {
                if step < 0 {
                    let step = step.abs() as usize;
                    let (start, stop) = ((stop + 1) as usize, (start + 1) as usize);
                    let list =
                        PyList::new(py, arr[start..stop].iter().rev().step_by(step).cloned());
                    Ok(list.into())
                } else {
                    let step = step as usize;
                    let (start, stop) = (start as usize, stop as usize);
                    let list = PyList::new(py, arr[start..stop].iter().step_by(step).cloned());
                    Ok(list.into())
                }
            }),
        }
    }

    fn normalize_index(&self, index: isize) -> u32 {
        if index < 0 {
            (self.__len__() as isize + index) as u32
        } else {
            index as u32
        }
    }

    pub fn insert_multiple_at(
        dst: &Array,
        txn: &mut Transaction,
        index: u32,
        src: Vec<PyObject>,
    ) -> PyResult<()> {
        let mut index = index;

        Python::with_gil(|py| {
            let mut iter = src
                .iter()
                .map(|element| CompatiblePyType::try_from(element.as_ref(py)))
                .peekable();
            while iter.peek().is_some() {
                let mut anys: Vec<Any> = Vec::default();
                while let Some(py_type) =
                    iter.next_if(|element| !matches!(element, Ok(CompatiblePyType::YType(_))))
                {
                    let any = Any::try_from(py_type?)?;
                    anys.push(any)
                }

                if !anys.is_empty() {
                    let len = anys.len() as u32;
                    dst.insert_range(txn, index, anys);
                    index += len;
                }

                while let Some(y_type) =
                    iter.next_if(|element| matches!(element, Ok(CompatiblePyType::YType(_))))
                {
                    dst.insert(txn, index, y_type?);
                    index += 1
                }
            }
            Ok(())
        })
    }

    fn py_iter(iterable: PyObject) -> PyResult<Vec<PyObject>> {
        Python::with_gil(|py| {
            iterable.as_ref(py).iter().and_then(|iterable| {
                iterable
                    .map(|element| {
                        element.map(|el| {
                            let el: PyObject = el.into();
                            el
                        })
                    })
                    .collect()
            })
        })
    }
}
#[derive(FromPyObject)]
pub enum Index<'a> {
    Int(isize),
    Slice(&'a PySlice),
}

/// Event generated by `YArray.observe` method. Emitted during transaction commit phase.
#[pyclass(unsendable)]
pub struct YArrayEvent {
    inner: *const ArrayEvent,
    txn: *const Transaction,
    target: Option<PyObject>,
    delta: Option<PyObject>,
}

impl YArrayEvent {
    pub fn new(event: &ArrayEvent, txn: &Transaction) -> Self {
        let inner = event as *const ArrayEvent;
        let txn = txn as *const Transaction;
        YArrayEvent {
            inner,
            txn,
            target: None,
            delta: None,
        }
    }

    fn inner(&self) -> &ArrayEvent {
        unsafe { self.inner.as_ref().unwrap() }
    }

    fn txn(&self) -> &Transaction {
        unsafe { self.txn.as_ref().unwrap() }
    }
}

#[pymethods]
impl YArrayEvent {
    /// Returns a current shared type instance, that current event changes refer to.
    #[getter]
    pub fn target(&mut self) -> PyObject {
        if let Some(target) = self.target.as_ref() {
            target.clone()
        } else {
            let target: PyObject =
                Python::with_gil(|py| YArray::from(self.inner().target().clone()).into_py(py));
            self.target = Some(target.clone());
            target
        }
    }

    fn __repr__(&mut self) -> String {
        let target = self.target();
        let delta = self.delta();
        let path = self.path();
        format!("YArrayEvent(target={target}, delta={delta}, path={path})")
    }

    /// Returns an array of keys and indexes creating a path from root type down to current instance
    /// of shared type (accessible via `target` getter).
    pub fn path(&self) -> PyObject {
        Python::with_gil(|py| self.inner().path().into_py(py))
    }

    /// Returns a list of text changes made over corresponding `YArray` collection within
    /// bounds of current transaction. These changes follow a format:
    ///
    /// - { insert: any[] }
    /// - { delete: number }
    /// - { retain: number }
    #[getter]
    pub fn delta(&mut self) -> PyObject {
        if let Some(delta) = &self.delta {
            delta.clone()
        } else {
            let delta: PyObject = Python::with_gil(|py| {
                let delta = self
                    .inner()
                    .delta(self.txn())
                    .into_iter()
                    .map(|change| Python::with_gil(|py| change.into_py(py)));
                PyList::new(py, delta).into()
            });
            self.delta = Some(delta.clone());
            delta
        }
    }
}

impl DefaultPyErr for PyIndexError {
    fn default_message() -> PyErr {
        PyIndexError::new_err("Index out of bounds.")
    }
}
