use pyo3::prelude::*;

// ---------- Main Util for analyzing formulas ----------
// Will take a formula string in R syntax and parse it into a structured format. This
// returned value will be used with the input polars df to create a model matrix.

use core::str;
use crate::models::utils::general_utils;

/// Function to parse a formula string and extract _____.
///
/// Args:
/// - `formula` (string): The formula string in R syntax.
///
/// Returns:
/// - A vector of FormulaTerm structs representing the parsed formula.
#[pyfunction]
#[pyo3(name = "_parse_formula")]
pub fn parse_formula(formula: &str) -> Result<Formula, FormulaError> {
    // 1) Split into dependent and independent variables using '~'.
    let (dependent_str, independent_str) = separate_x_y(formula)?;

    // 2) Identify individual terms
        // 2a) Turn the dependent variable into a term object.
        // 2b) Split the independent variables by '+' and '-' to get a vector of 
        // strings, then turn these into terms. Remember to 
        // remove any duplicated terms.
    let terms: (FormulaTerm, Vec<FormulaTerm>) = tokenize_formula(dependent_str, independent_str)?;
    
    // 3) Return Formula struct with:
        // - Original formula string
        // - Dependent variable term
        // - Vector of independent variable terms
    let result: Formula = Formula::new(formula, terms.0, terms.1);
    return Ok(result)
}


// ---------- Helper functions ----------

/// Function to separate a formula into independent and dependent variables
/// 
/// Args:
/// - 'formula' (&str): The formula string in R syntax.
/// 
/// Returns:
/// - A Result containing a tuple of the dependent variable and independent variable 
/// strings, or an error if the formula is empty or has tilde errors.
fn separate_x_y(formula: &str) -> Result<(&str, &str), FormulaError> {
    // Check for an empty string
    if formula.trim().is_empty() {
        return Err(FormulaError::EmptyFormula);
    }

    // Find the position of the '~' and split the formula into two parts: 
    //      before and after the '~'
    let tilde_pos: usize = formula.find('~').ok_or(FormulaError::MissingTilde)?;
    if formula[tilde_pos + 1..].contains('~') { return Err(FormulaError::MultipleTildes); }

    let before: &str = formula[..tilde_pos].trim();
    let after: &str = formula[tilde_pos + 1..].trim();
    
    Ok((before, after))
}

/// Function to identify individual terms in the two parts of a split formula string.
/// 
/// Args:
/// - 'dependent_str' (&str): The dependent variable string.
/// - 'independent_str' (&str): The independent variable string.
/// 
/// Returns:
/// - A Result containing a tuple of the dependent variable FormulaTerm, and a vector for 
/// the independent variable FormulaTerms. .
fn tokenize_formula(dependent_str: &str, independent_str: &str) -> Result<(FormulaTerm, Vec<FormulaTerm>), FormulaError> {
    // Tokenize the dependent variable
    let dependent_term: FormulaTerm = tokenize_y(dependent_str)?;

    // Tokenize the independent variables
    let independent_terms: Vec<FormulaTerm> = tokenize_independent(independent_str)?;

    let all_terms: (FormulaTerm, Vec<FormulaTerm>) = (dependent_term, independent_terms);
    Ok(all_terms)
}

/// Function to tokenize the independent variable string.
/// 
/// Args:
/// - 'independent_str' (&str): The independent variable string.
///
/// Returns:
/// - A Result containing a vector of FormulaTerm objects for the independent variables,
/// or an error if the independent variable string is empty or invalid.
fn tokenize_independent(independent_str: &str) -> Result<Vec<FormulaTerm>, FormulaError> {
    let trimmed: &str = independent_str.trim();
    if trimmed.is_empty() {
        return Err(FormulaError::EmptyIndependent);
    }
    
    let mut all_terms: Vec<FormulaTerm> = Vec::new();
    let mut current_term: String = String::new();
    let mut current_operator: Option<char> = None;
    
    for ch in trimmed.chars() {
        match ch {
            '+' | '-' => {
                // Process current term if not empty
                if !current_term.trim().is_empty() {
                    let expanded = expand_term(current_term.trim(), current_operator)?;
                    all_terms.extend(expanded);
                    current_term.clear();
                }
                current_operator = Some(ch)
            }
            _ => {
                current_term.push(ch);
            }
        }
    }
    
    // Handle last term
    if !current_term.trim().is_empty() {
        let expanded: Vec<FormulaTerm> = expand_term(current_term.trim(), current_operator)?;
        all_terms.extend(expanded);
    }
    
    Ok(clean_up_terms(&all_terms))
}

/// Function to expand a term string and relevant operator into a vector of 
/// FormulaTerm objects. This handles plain terms and interaction terms, will 
/// soon handle transformations as well(but not yet).
///
/// Args:
/// - `term_str` (string): The term string to expand, e.g., "x1*x2" or "x1:x2".
/// - 'operator' (Option<char>): The operator character, e.g. "+" or "-"
/// 
/// Returns:
/// - A Result containing a vector of FormulaTerm objects, or an error if the 
/// term string is invalid.
fn expand_term(term_str: &str, operator: Option<char>) -> Result<Vec<FormulaTerm>, FormulaError> {
    let mut expanded_term: Vec<FormulaTerm> = if term_str.contains('*') {
        // Handle multiplication expansion: x1*x2 -> [x1, x2, x1:x2]
        expand_multiplication(term_str)?
    } else if term_str.contains(':') {
        // Handle interaction: x1:x2 -> [x1:x2]
        vec![handle_interaction(term_str)?]
    } else if general_utils::is_numeric(term_str) {
        vec![FormulaTerm::create_intercept_term(term_str)?]
    } else {
        // Simple term: x1 -> [x1]
        vec![FormulaTerm::create_simple_term(term_str)?]
    };

    // Apply subtraction if necessary
    if operator == Some('-') {
        for term in &mut expanded_term {
            term.subtracted = true;
        }
    }

    return Ok(expanded_term)
}

/// Function to handle interaction terms.
/// 
////// Args:
/// - `term_str` (string): The term string to expand, e.g., "x1:x2".
/// 
/// Returns:
/// - A Result containing a FormulaTerm object, or an error if the
/// term string is invalid.
fn handle_interaction(term_str: &str) -> Result<FormulaTerm, FormulaError> {
    let variables: Vec<&str> = term_str.split(':').map(str::trim).collect();
    
    if variables.len() != 2 {
        return Err(FormulaError::InvalidTerm(term_str.to_string()));
    }
    
    let var1: &str = variables[0];
    let var2: &str = variables[1];
    
    Ok(FormulaTerm::create_interaction_term(var1, var2)?)
}

/// Function to handle terms that are multiplied together.
/// 
////// Args:
/// - `term_str` (string): The term string to expand, e.g., "x1*x2".
/// 
/// Returns:
/// - A Result containing a vector of FormulaTerm objects, or an error if the
/// term string is invalid.
fn expand_multiplication(term_str: &str) -> Result<Vec<FormulaTerm>, FormulaError> {
    let variables: Vec<&str> = term_str.split('*').map(str::trim).collect();
    
    if variables.len() != 2 {
        return Err(FormulaError::InvalidTerm(term_str.to_string()));
    }
    
    let var1: &str = variables[0];
    let var2: &str = variables[1];
    
    Ok(vec![
        FormulaTerm::create_simple_term(var1)?,
        FormulaTerm::create_simple_term(var2)?,
        FormulaTerm::create_interaction_term(var1, var2)?,
    ])
}

/// Function to tokenize the dependent variable string.
/// 
/// Args:
/// - 'dependent_str' (&str): The dependent variable string.
/// 
/// Returns:
/// - A Result containing a FormulaTerm for the dependent variable, or an error if the
/// dependent variable is empty.
fn tokenize_y(dependent_str: &str) -> Result<FormulaTerm, FormulaError> {
    let dependent_str = dependent_str.trim();

    // Check for empty dependent variable
    if dependent_str.is_empty() {
        return Err(FormulaError::EmptyDependent);
    }

    // Create a FormulaTerm for the dependent variable
    Ok(FormulaTerm::create_dependent_term(dependent_str)?)
}

/// Function to:
/// - Remove any subtracted or duplicated terms from a vector of FormulaTerm 
/// objects.
/// - Also figures out the intercept term. If 0, will remove it. If some other 
/// term(s), sums them.
/// 
/// Args:
/// - `terms` (&[FormulaTerm]): The vector of FormulaTerm objects to process.
/// 
/// Returns:
/// - A vector of FormulaTerm objects with subtracted and duplicated terms removed.
fn clean_up_terms(terms: &[FormulaTerm]) -> Vec<FormulaTerm> {
    // 1) Figure out intercept term
    let intercept_term: Option<FormulaTerm> = get_intercept_term(terms);

    // 2) Remove subtracted/duplicated terms
    let relevant_terms: Vec<FormulaTerm> = get_relevant_terms(terms);
    
    // 3) Put everything together
    //     - If intercept term exists, add it to the front of the vector.
    //     - If no intercept term, just return the relevant terms.
    let mut terms: Vec<FormulaTerm> = Vec::new();
    if let Some(intercept) = intercept_term {
        terms.push(intercept);
    }
    for term in relevant_terms {
        if !term.intercept {
            terms.push(term);
        }
    }
    
    terms
}

/// Function to remove duplicated and subtracted terms from a vector of FormulaTerm 
/// objects.
/// 
/// Args:
/// - `terms` (&Vec<FormulaTerm>): The vector of FormulaTerm objects to process.
///
/// Returns:
/// - A vector of FormulaTerm objects with subtracted and duplicated terms removed.
fn get_relevant_terms(terms: &[FormulaTerm]) -> Vec<FormulaTerm> {
    use indexmap::IndexMap;
    
    // 1): Group terms by name to handle duplicates and subtractions
    let mut term_groups: IndexMap<String, Vec<FormulaTerm>> = IndexMap::new();
    
    for term in terms {
        term_groups.entry(term.name.clone())
            .or_insert_with(Vec::new)
            .push(term.clone());
    }

    // 2): Process each group of terms with the same name
    let mut result: Vec<FormulaTerm> = Vec::new();
    
    for (_name, mut group) in term_groups {
        let has_subtracted: bool = group.iter().any(|term: &FormulaTerm| term.subtracted);
        
        if !has_subtracted && !group.is_empty() {
            result.push(group.remove(0)); // Take ownership by removing from vec
        }
    }

    return result;
}

/// Function to get the intercept term from a vector of FormulaTerm objects. <br>
/// If any intercept term(s) exists that are non-zero, we will have an intercept.
/// If no intercept term exists, we will create one with the name "1". If only
/// zero value intercept terms exist, we will not return an intercept term.
///
/// Args:
/// - `terms` (&[FormulaTerm]): The vector of FormulaTerm objects to process.
///
/// Returns:
/// - An Option containing the intercept term if it exists, or None if there is no intercept
/// term.
fn get_intercept_term(terms: &[FormulaTerm]) -> Option<FormulaTerm> {
    // Check if there is an intercept term in the vector. If none, make 
    // intercept term.
    // Find all intercept terms
    let intercept_terms: Vec<&FormulaTerm> = terms.iter()
        .filter(|term| term.intercept)
        .collect();

    if intercept_terms.is_empty() {
        // No intercept terms found - return default intercept with name "1"
        return Some(FormulaTerm::create_intercept_term(&"1".to_string()).ok()?)
    } else {
        let has_non_zero = intercept_terms.iter()
            .any(|term| term.name != "0");
        if has_non_zero {
            // At least one intercept is not "0" - return intercept with name "1"
            return Some(FormulaTerm::create_intercept_term(&"1".to_string()).ok()?)
        } else {
            // All intercept terms have name "0" - return None (no intercept)
            return None
        }
    }
}

// ---------- Formula structs & enums ----------

#[derive(Debug, Clone)]
/// Struct to represent a parsed formula. This will be used to make the model 
/// matrix later, and needs to contain all of the necessary info to do so.
#[pyclass]
pub struct Formula {
    original: String,
    dependent: FormulaTerm,
    independent: Vec<FormulaTerm>,
}

impl Formula {
    fn new(original_str: &str, dependent: FormulaTerm, independent: Vec<FormulaTerm>) -> Self {
        Formula {
            original: original_str.to_string(),
            dependent,
            independent,
        }
    }
}

#[pymethods]
impl Formula {
    fn __repr__(&self) -> String {
        format!("{} ~ {}", self.dependent.name, self.independent.iter()
            .map(|term| term.name.clone())
            .collect::<Vec<String>>()
            .join(" + "))
    }
    
    fn __str__(&self) -> String {
        format!("{} ~ {}", self.dependent.name, self.independent.iter()
            .map(|term| term.name.clone())
            .collect::<Vec<String>>()
            .join(" + "))
    }
    
    // Optional: Add a Python constructor if needed
    #[new]
    fn py_new(original_str: String, dependent: FormulaTerm, independent: Vec<FormulaTerm>) -> Self {
        Formula {
            original: original_str,
            dependent,
            independent,
        }
    }
}

#[derive(Debug, Clone)]
#[pyclass]
struct FormulaTerm {
    name: String,
    dependent: bool, // Whether this term is a dependent variable
    subtracted: bool, // Whether this term is subtracted from the model
    intercept: bool, // Whether this term is an intercept term
    interaction: bool, // Whether this term is an interaction term
    // transformation: Option<TermTransformation>, // Optional transformation (e.g., log, square). This will not be implemented for now, but later.
}

impl FormulaTerm {
    fn new(name: &str) -> Result<Self, FormulaError> {
        if name.is_empty() {
            return Err(FormulaError::EmptyIndependent);
        }
        
        Ok(FormulaTerm {
            name: name.trim().to_string(),
            dependent: false,
            subtracted: false,
            intercept: false,
            interaction: false,
            // transformation: None,
        })
    }

    // Internal methods to set properties of the term

    fn as_dependent(mut self) -> Self {
        self.dependent = true;
        self
    }
    
    fn as_intercept(mut self) -> Self {
        self.intercept = true;
        self
    }
    
    fn as_interaction(mut self) -> Self {
        self.interaction = true;
        self
    }

    // Factory methods to create specific types of terms

    fn create_simple_term(name: &str) -> Result<Self, FormulaError> {
        Self::new(name)
    }

    fn create_dependent_term(name: &str) -> Result<Self, FormulaError> {
        Ok(Self::new(name)?.as_dependent())
    }

    fn create_intercept_term(name: &str) -> Result<Self, FormulaError> {
        Ok(Self::new(&name)?.as_intercept())
    }

    fn create_interaction_term(var1: &str, var2: &str) -> Result<Self, FormulaError> {
        let name: String = format!("{}:{}", var1, var2);
        Ok(Self::new(&name)?.as_interaction())
    }
}

// enum TermTransformation {
//     Log,
//     Square,
//     Custom(String) // Custom transformation
// }

// ---------- Errors ----------

use pyo3::exceptions::PyValueError;

/// Error type for formula parsing issues.
#[derive(Debug, Clone)]
pub enum FormulaError {
    EmptyFormula,
    MissingTilde,
    MultipleTildes,
    EmptyDependent,
    EmptyIndependent,
    InvalidTerm(String)
}


impl std::fmt::Display for FormulaError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            FormulaError::EmptyFormula => write!(f, "Formula cannot be empty"),
            FormulaError::MissingTilde => write!(f, "Formula must contain '~' to separate dependent and independent variables"),
            FormulaError::MultipleTildes => write!(f, "Formula cannot contain multiple '~' characters"),
            FormulaError::EmptyDependent => write!(f, "Dependent variable cannot be empty"),
            FormulaError::EmptyIndependent => write!(f, "Independent variables cannot be empty"),
            FormulaError::InvalidTerm(term) => write!(f, "Invalid term found in formula: '{}'", term)
        }
    }
}

impl std::convert::From<FormulaError> for PyErr {
    fn from(err: FormulaError) -> PyErr {
        // All errors map best to ValueError in python
        PyValueError::new_err(err.to_string())
    }
}

impl std::error::Error for FormulaError {}

