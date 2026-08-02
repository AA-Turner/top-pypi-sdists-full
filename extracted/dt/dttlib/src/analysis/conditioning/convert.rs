//! Pipeline converters from real types to f64, and complex types to c128
//! These are run at the front of an analysis pipeline, which are all done on f64 and c128
//!

use crate::AccumulationStats;
use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::errors::DTTError;
use futures::FutureExt;
use num::cast::AsPrimitive;
use num::{Complex, Float};
use pipeline_macros::box_async;
use pipelines::complex::{c64, c128};
use pipelines::stateless::Stateless1;
use pipelines::{PipeDataPrimitive, PipeResult, PipelineSubscriber};
use std::fmt::Debug;
use std::sync::Arc;
use user_messages::UserMsgProvider;

pub trait ConvertTo<T: Copy> {
    fn convert_to(self) -> T;
}

impl<T: Copy + 'static> ConvertTo<T> for i8
where
    i8: AsPrimitive<T>,
    T: Float,
{
    fn convert_to(self) -> T {
        if self == Self::MAX {
            T::nan()
        } else {
            self.as_()
        }
    }
}

impl<T: Copy + 'static> ConvertTo<T> for i16
where
    i16: AsPrimitive<T>,
    T: Float,
{
    fn convert_to(self) -> T {
        if self == Self::MAX {
            T::nan()
        } else {
            self.as_()
        }
    }
}

impl<T: Copy + 'static> ConvertTo<T> for i32
where
    i32: AsPrimitive<T>,
    T: Float,
{
    fn convert_to(self) -> T {
        if self == Self::MAX {
            T::nan()
        } else {
            self.as_()
        }
    }
}

impl<T: Copy + 'static> ConvertTo<T> for i64
where
    i64: AsPrimitive<T>,
    T: Float,
{
    fn convert_to(self) -> T {
        if self == Self::MAX {
            T::nan()
        } else {
            self.as_()
        }
    }
}

impl<T: Copy + 'static> ConvertTo<T> for f32
where
    f32: AsPrimitive<T>,
{
    fn convert_to(self) -> T {
        self.as_()
    }
}

impl<T: Copy + 'static> ConvertTo<T> for f64
where
    f64: AsPrimitive<T>,
{
    fn convert_to(self) -> T {
        self.as_()
    }
}

impl<T: Copy + 'static> ConvertTo<T> for u8
where
    u8: AsPrimitive<T>,
    T: Float,
{
    fn convert_to(self) -> T {
        if self == Self::MAX {
            T::nan()
        } else {
            self.as_()
        }
    }
}

impl<T: Copy + 'static> ConvertTo<T> for u16
where
    u16: AsPrimitive<T>,
    T: Float,
{
    fn convert_to(self) -> T {
        if self == Self::MAX {
            T::nan()
        } else {
            self.as_()
        }
    }
}

impl<T: Copy + 'static> ConvertTo<T> for u32
where
    u32: AsPrimitive<T>,
    T: Float,
{
    fn convert_to(self) -> T {
        if self == Self::MAX {
            T::nan()
        } else {
            self.as_()
        }
    }
}

impl<T: Copy + 'static> ConvertTo<T> for u64
where
    u64: AsPrimitive<T>,
    T: Float,
{
    fn convert_to(self) -> T {
        if self == Self::MAX {
            T::nan()
        } else {
            self.as_()
        }
    }
}

impl<T: Copy + 'static> ConvertTo<Complex<T>> for c64
where
    f32: AsPrimitive<T>,
{
    fn convert_to(self) -> Complex<T> {
        Complex::new(self.re.as_(), self.im.as_())
    }
}

impl<T: Copy + 'static> ConvertTo<Complex<T>> for c128
where
    f64: AsPrimitive<T>,
{
    fn convert_to(self) -> Complex<T> {
        Complex::new(self.re.as_(), self.im.as_())
    }
}

#[box_async]
fn convert<'a, T, U>(
    _rc: Box<dyn UserMsgProvider>,
    _name: String,
    _config: &(),
    input: Arc<TimeDomainArray<T>>,
) -> PipeResult<TimeDomainArray<U>>
where
    U: PipeDataPrimitive + Copy,
    T: PipeDataPrimitive + Copy + ConvertTo<U> + Debug,
{
    let new_data: Vec<_> = input.data.iter().map(|x| x.clone().convert_to()).collect();
    Arc::new(TimeDomainArray {
        start_gps_pip: input.start_gps_pip,
        period_pip: input.period_pip,
        data: new_data,
        accumulation_stats: AccumulationStats::default(),
        total_gap_size: input.total_gap_size,
        id: input.id.clone(),
        unit: input.unit.clone(),
        real_end_gps_pip: input.real_end_gps_pip,
    })
    .into()
}

pub async fn start_pipe_converter<T: PipeDataPrimitive + Copy, U: PipeDataPrimitive + Copy>(
    rc: Box<dyn UserMsgProvider>,
    name: impl Into<String>,
    input: &PipelineSubscriber<TimeDomainArray<T>>,
) -> Result<PipelineSubscriber<TimeDomainArray<U>>, DTTError>
where
    T: ConvertTo<U> + Debug,
{
    Ok(Stateless1::create(rc.ump_clone(), name.into(), convert, (), input).await?)
}
