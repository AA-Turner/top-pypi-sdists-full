mod pretty;
mod simple;

pub use pretty::Pretty;
pub use simple::Simple;

pub trait Print<Printer> {
    /// Formats the object using the given formatter.
    fn print(&self, printer: Printer);
}

impl<T, P> Print<P> for Vec<T>
where
    T: Print<P>,
    P: Copy,
{
    fn print(&self, printer: P) {
        for item in self {
            item.print(printer);
        }
    }
}
