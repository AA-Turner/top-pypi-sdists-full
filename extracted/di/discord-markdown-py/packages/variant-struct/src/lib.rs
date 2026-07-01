use proc_macro::TokenStream;
use quote::{format_ident, quote};
use syn::{Data, DeriveInput, Fields, Ident, LitStr, parse_macro_input};

#[proc_macro_derive(VariantStruct, attributes(variant_struct))]
pub fn derive_variant_struct(input: TokenStream) -> TokenStream {
	let input = parse_macro_input!(input as DeriveInput);
	let enum_name = &input.ident;
	let vis = &input.vis;

	// Container attr: #[variant_struct(name = "ColorMap")]
	let mut struct_name: Option<Ident> = None;
	for attr in &input.attrs {
		if attr.path().is_ident("variant_struct") {
			let _ = attr.parse_nested_meta(|meta| {
				if meta.path.is_ident("name") {
					let lit: LitStr = meta.value()?.parse()?;
					struct_name = Some(format_ident!("{}", lit.value()));
				}
				Ok(())
			});
		}
	}
	let struct_name = struct_name.unwrap_or_else(|| format_ident!("{}Struct", enum_name));

	let variants = match &input.data {
		Data::Enum(data) => &data.variants,
		_ => {
			return syn::Error::new_spanned(enum_name, "VariantStruct only works on enums")
				.to_compile_error()
				.into();
		}
	};

	let mut fields = Vec::new();
	let mut patterns = Vec::new();

	for v in variants {
		let vname = &v.ident;

		// Per-variant attr: #[variant_struct(rename = "dark_gray")]
		let mut rename: Option<Ident> = None;
		for attr in &v.attrs {
			if attr.path().is_ident("variant_struct") {
				let _ = attr.parse_nested_meta(|meta| {
					if meta.path.is_ident("rename") {
						let lit: LitStr = meta.value()?.parse()?;
						rename = Some(format_ident!("{}", lit.value()));
					}
					Ok(())
				});
			}
		}
		let field =
			rename.unwrap_or_else(|| format_ident!("{}", to_snake_case(&vname.to_string())));

		let pattern = match &v.fields {
			Fields::Unit => quote! { #enum_name::#vname },
			Fields::Unnamed(_) => quote! { #enum_name::#vname(..) },
			Fields::Named(_) => quote! { #enum_name::#vname { .. } },
		};

		fields.push(field);
		patterns.push(pattern);
	}

	let variant_exprs: Vec<_> = variants
		.iter()
		.map(|v| {
			let vname = &v.ident;
			match &v.fields {
				Fields::Unit => quote! { #enum_name::#vname },
				// Non-unit variants can't be constructed without payload data,
				// so we skip them in the iterator. See notes below.
				_ => quote! { compile_error!(
					"iter_variants requires all variants to be unit variants"
				) },
			}
		})
		.collect();

	quote! {
		#[derive(Debug, Clone)]
		#vis struct #struct_name<T> {
			#(pub #fields: T,)*
		}

		impl<T> #struct_name<T> {
			pub fn from_fn<F: FnMut() -> T>(mut f: F) -> Self {
				Self { #(#fields: f(),)* }
			}

			pub fn get(&self, variant: &#enum_name) -> &T {
				match variant {
					#(#patterns => &self.#fields,)*
				}
			}

			pub fn get_mut(&mut self, variant: &#enum_name) -> &mut T {
				match variant {
					#(#patterns => &mut self.#fields,)*
				}
			}

			pub fn set(&mut self, variant: &#enum_name, value: T) {
				*self.get_mut(variant) = value;
			}

			pub fn replace(&mut self, variant: &#enum_name, value: T) -> T {
				::core::mem::replace(self.get_mut(variant), value)
			}

			pub fn iter(&self) -> impl Iterator<Item = &T> {
				[#(&self.#fields),*].into_iter()
			}

			pub fn iter_variants(&self) -> impl Iterator<Item = (#enum_name, &T)> {
				[#((#variant_exprs, &self.#fields)),*].into_iter()
			}

			pub fn iter_variants_mut(&mut self) -> impl Iterator<Item = (#enum_name, &mut T)> {
				[#((#variant_exprs, &mut self.#fields)),*].into_iter()
			}
		}

		impl<T: Default> Default for #struct_name<T> {
			fn default() -> Self {
				Self { #(#fields: T::default(),)* }
			}
		}
	}
	.into()
}

fn to_snake_case(s: &str) -> String {
	let mut out = String::with_capacity(s.len() + 4);
	for (i, ch) in s.chars().enumerate() {
		if ch.is_uppercase() {
			if i > 0 {
				out.push('_');
			}
			out.extend(ch.to_lowercase());
		} else {
			out.push(ch);
		}
	}
	out
}
