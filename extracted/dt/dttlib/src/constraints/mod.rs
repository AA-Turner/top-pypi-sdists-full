//! A generic struct for a constraint that takes a single input and either passes or fails.

use crate::run_context::RunContext;
use user_messages::Severity;

pub struct Constraint<T> {
    /// short slug used as a unique identifier for UserMessages
    tag: &'static str,

    /// Description to be shown to the user in case the constraint is not met.
    description: &'static str,

    /// Severity of the constraints violation
    pub severity: Severity,

    /// If the function returns true, the constraint is met
    test: fn(&T) -> bool,
}

impl<T> Constraint<T> {
    pub const fn new(
        tag: &'static str,
        description: &'static str,
        severity: Severity,
        test: fn(&T) -> bool,
    ) -> Self {
        Self {
            tag,
            description,
            severity,
            test,
        }
    }

    /// Test the constraint.
    /// Persistently sets a user message if the constraint is not met,
    /// And clears it once the constraint is met again.
    /// return the true if constraint is met
    pub fn check(&self, rc: Box<RunContext>, t: &T) -> bool {
        let result = (self.test)(t);
        if result {
            rc.user_messages.clear_message(self.tag);
        } else {
            rc.user_messages
                .set_message(self.severity, self.tag, String::from(self.description));
        };
        result
    }
}

/// Check a slice of constraints against a value
/// Returns false on failure of any constraint having severity of Error or greater
/// Otherwise returns true.  In particular, if all failured constraints
/// are of severity Warning, the function will still return true.
pub fn check_constraint_list<T>(
    rc: Box<RunContext>,
    constraint_list: &[Constraint<T>],
    value: &T,
) -> bool {
    let mut go_ahead = true;
    for c in constraint_list.iter() {
        let result = c.check(rc.clone(), value);
        if !result && c.severity >= Severity::Error {
            go_ahead = false;
        }
    }
    go_ahead
}
