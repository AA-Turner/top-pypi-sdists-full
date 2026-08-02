use crate::errors::DTTError;

use crate::user::{DTT, UserOutputReceiver, start_user_process};

/// Initialize operation with an existing runtime
/// starts supervisor and all other permanent tasks
pub fn tokio_init(runtime: &tokio::runtime::Handle) -> Result<(DTT, UserOutputReceiver), DTTError> {
    let uc_items = DTT::create(runtime.clone());
    let uc = uc_items.0;
    uc.runtime.spawn(start_user_process(uc_items.1, uc_items.2));
    Ok((uc, uc_items.3))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_startup() {
        let runtime = tokio::runtime::Runtime::new().unwrap();
        let (mut uc, _) = tokio_init(runtime.handle()).unwrap();

        uc.no_op().unwrap();
    }
}
