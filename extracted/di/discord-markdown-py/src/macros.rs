// The following types do not get macros as their raw implementations are
// simpler / more straightforward to use compared to a macro implementation
//
// ---- block ----
// - Empty,
//
// ---- inline ----
// - Timestamp(Timestamp),
// - Mention(Mention<'a>),

/// Create a vec wrapped in a span, and also wrap each element in a span.
#[macro_export]
macro_rules! spanned_vec {
    [] => {
        $crate::span::Spanned::default()
    };
	[$($children:expr),+ $(,)?] => {
		$crate::span::Spanned {
			value: vec![$($crate::spanned!($children)),*],
			span: Default::default(),
		}
	};
}

/// Wrap an item in a span.
#[macro_export]
macro_rules! spanned {
	($value: expr) => {
		$crate::span::Spanned {
			value: $value,
			span: Default::default(),
		}
	};
}

/// Create a heading.
#[macro_export]
macro_rules! heading {
    ($level: literal, $text_content: literal) => {
        heading!(__private $level, $crate::spanned_vec![$crate::text!($text_content)])
    };
    ($level: literal, [$($children: expr),+ $(,)?]) => {
        heading!(__private $level, $crate::spanned_vec![$($children),*])
    };
    (__private $level: literal, $children: expr) => {
        $crate::node::Block::Heading($crate::node::block::heading::Heading {
            level: $level,
            content: $children,
        })
    }
}

// list!(ordered, [
//     list_item!(1: "asd"),
//     list_item!(2: underline!("underlined!")),
//     list_item!(3: [
//         unstyled!("asd"),
//         list!(unordered, [
//             list_item!(- "cats"),
//             list_item!(- "dogs"),
//             list_item!(- "bananas")
//         ])
//     ])
// ]);
/// Create a list.
#[macro_export]
macro_rules! list {
    (- [$($list_item: expr),+ $(,)?]) => {
        $crate::node::Block::List($crate::node::block::list::List {
            kind: $crate::node::block::list::Type::Unordered,
            items: $crate::list_items!($($list_item),*)
        })
    };
    ($bullet_number: literal: [$($list_item: expr),+ $(,)?]) => {
        $crate::node::Block::List($crate::node::block::list::List {
            kind: $crate::node::block::list::Type::Ordered(
                ::std::num::NonZero::new($bullet_number).unwrap()
            ),
            items: $crate::list_items!($($list_item),*)
        })
    };
}

/// Create a list item.
#[macro_export]
macro_rules! list_item {
    ($text_content: literal) => {
        list_item!(__private $crate::spanned_vec![$crate::paragraph!($text_content)])
    };
    [$($children: expr),+ $(,)?] => {
        list_item!(__private $crate::spanned_vec![$($children),*])
    };
    ($single_item: expr) => {
        list_item!(__private $crate::spanned_vec![$crate::paragraph!($single_item)])
    };
    (__private $children: expr) => {
        $crate::node::block::list::item::Item {
            content: $children
        }
    };
}

/// Create many list items.
#[macro_export]
macro_rules! list_items {
    [$($children: expr),*] => {
        $crate::span::Spanned {
            value: vec![$($children),*],
            span: Default::default(),
        }
    };
}

/// Create a quote.
#[macro_export]
macro_rules! quote {
    ($text_content: literal) => {
        quote!(__private vec![quote_line!($text_content)])
    };
    ($( $lines: expr),+ $(,)?) => {
        quote!(__private vec![$($lines),*])
    };
    (__private $lines: expr) => {
        $crate::Node::Quote($crate::node::block::quote::Quote {
            lines: $lines
        })
    };
}

/// Create a paragraph.
#[macro_export]
macro_rules! paragraph {
    ( $text_content: literal ) => {
        $crate::paragraph!($crate::text!($text_content))
    };
    ($($children: expr),* $(,)?) => {
        $crate::node::Block::Paragraph($crate::spanned_vec![$($children),*])
    };
}

// ======= Inline =======

/// Create text.
#[macro_export]
macro_rules! text {
	( $text_content: literal ) => {
		$crate::node::Inline::Text($text_content.into())
	};
}

// ======= Modifier =======

/// Create a modifier node of the given [`crate::node::modifier::ModifierKind`].
#[macro_export]
macro_rules! modifier {
    ( $kind: ident, $text_content: literal ) => {
        $crate::modifier!($kind, $crate::text!($text_content))
    };
    ( $kind: ident, $($children: expr),+ $(,)? ) => {
        $crate::node::Inline::$kind($crate::spanned_vec![$($children),*])
    };
}

/// Create bold.
#[macro_export]
macro_rules! bold {
    ( $($tokens: tt)+ ) => {
        $crate::modifier!(Bold, $($tokens)+)
    };
}

/// Create italic.
#[macro_export]
macro_rules! italic {
    ( $($tokens: tt)+ ) => {
        $crate::modifier!(Italic, $($tokens)+)
    };
}

/// Create underline.
#[macro_export]
macro_rules! underline {
    ( $($tokens: tt)+ ) => {
        $crate::modifier!(Underline, $($tokens)+)
    };
}

/// Create strikethrough.
#[macro_export]
macro_rules! strikethrough {
    ( $($tokens: tt)+ ) => {
        $crate::modifier!(Strikethrough, $($tokens)+)
    };
}

/// Create spoiler, with id zero unless given as `id = …;` first.
#[macro_export]
macro_rules! spoiler {
    ( id = $id: expr; $text_content: literal ) => {
        $crate::spoiler!(id = $id; $crate::text!($text_content))
    };
    ( id = $id: expr; $($children: expr),+ $(,)? ) => {
        $crate::node::Inline::Spoiler($crate::node::modifier::spoiler::Spoiler {
            id: $crate::node::Id($id),
            content: $crate::spanned_vec![$($children),*],
        })
    };
    ( $($tokens: tt)+ ) => {
        $crate::spoiler!(id = 0; $($tokens)+)
    };
}

/// Create code.
#[macro_export]
macro_rules! code {
	( $text_content: literal ) => {
		$crate::node::Inline::Code($text_content.into())
	};
}

/// Create a code block.
#[macro_export]
macro_rules! code_block {
    ( $text_content: literal ) => {
       code_block!(__private $text_content, None)
    };
    ( language=$language: literal, $text_content: literal) => {
         code_block!(__private $text_content, Some($language.into()))
    };
    (__private $text_content: literal, $language: expr) => {
        $crate::node::Inline::CodeBlock($crate::node::inline::code_block::CodeBlock {
            language: $language,
            content: $text_content.to_string()
        })
    };
}

/// Create a custom or Unicode emoji.
#[macro_export]
macro_rules! emoji {
    // Unicode
    ($unicode: literal) => {
       $crate::node::Inline::Emoji($crate::node::inline::emoji::Emoji::Unicode($unicode.into()))
    };

    // Custom
    (id=$id: literal, name=$name: literal) => {
       emoji!(__private $id, $name, false)
    };
    (id=$id: literal, name=$name: literal, animated) => {
       emoji!(__private $id, $name, true)
    };
    (__private $id: literal, $name: literal, $animated: expr) => {
       $crate::node::Inline::Emoji($crate::node::inline::emoji::Emoji::Custom(
           $crate::node::inline::emoji::custom::Custom {
               id: $id,
               name: $name.into(),
               animated: $animated
           }
       ))
    };
}

/// Create a link.
#[macro_export]
macro_rules! link {
    ( $target: literal) => {
        link!(__private $target, None, None)
    };
    ( $target: literal, title=$title: literal) => {
        link!(__private $target, Some($title), None)
    };
    ( $target: literal, [$($children: expr),+ $(,)?]) => {
        link!(__private $target, None, Some($crate::spanned_vec![$($children),*]))
    };
    ( $target: literal, title=$title: literal, [$($children: expr),+ $(,)?]) => {
        link!(__private $target, Some($title), Some(vec![$($children),*]))
    };

    (__private $target: literal, $title: expr, $children: expr) => {
        $crate::node::Inline::Link($crate::node::inline::link::Link {
            url: $target.parse().unwrap(),
            text: $children,
            title: $title
        })
    };
}
