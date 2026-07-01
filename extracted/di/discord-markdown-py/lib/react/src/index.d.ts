import type {
	AnyNode,
	Block,
	Bold,
	Code,
	CodeBlock,
	Emoji,
	Heading,
	Italic,
	Link,
	List,
	ListItem,
	Mention,
	Paragraph,
	Quote,
	Small,
	Spoiler,
	Strikethrough,
	Text,
	Timestamp,
	Underline,
} from "@discord/markdown-types";
import type React from "react";

type NodeRenderProps<N, P> = P & {
	siblings: AnyNode[];
	index: number;
	node: N;
};
type NodeRenderPropsWithChildren<N, P = unknown> = React.PropsWithChildren<
	NodeRenderProps<N, P>
>;

// inline
export type BoldProps = NodeRenderPropsWithChildren<Bold>;
export type ItalicProps = NodeRenderPropsWithChildren<Italic>;
export type UnderlineProps = NodeRenderPropsWithChildren<Underline>;
export type StrikethroughProps = NodeRenderPropsWithChildren<Strikethrough>;
export type SpoilerProps = NodeRenderPropsWithChildren<Spoiler>;
export type EmojiProps = NodeRenderProps<Emoji, Emoji["value"]>;
export type TimestampProps = NodeRenderProps<Timestamp, Timestamp["value"]>;
export type MentionProps = NodeRenderProps<Mention, Mention["value"]>;
export type LinkProps = NodeRenderPropsWithChildren<Link, Link["value"]>;
export type CodeProps = NodeRenderPropsWithChildren<Code>;
export type CodeBlockProps = NodeRenderProps<CodeBlock, CodeBlock["value"]>;

export type InlineProps =
	| BoldProps
	| ItalicProps
	| UnderlineProps
	| StrikethroughProps
	| SpoilerProps
	| EmojiProps
	| TimestampProps
	| MentionProps
	| LinkProps
	| CodeProps
	| CodeBlockProps;

// block
export type HeadingProps = NodeRenderPropsWithChildren<
	Heading,
	{ level: 1 | 2 | 3 }
>;
export type ListProps = NodeRenderPropsWithChildren<List, List["value"]>;
export type QuoteProps = NodeRenderPropsWithChildren<Quote>;
export type SmallProps = NodeRenderPropsWithChildren<Small>;

export type BlockProps = HeadingProps | ListProps | QuoteProps | SmallProps;

// top-level
export type TextProps = NodeRenderPropsWithChildren<Text>;
export type ParagraphProps = NodeRenderPropsWithChildren<Paragraph>;
export type EmptyProps = NodeRenderProps<never, Record<string, never>>;
export type ListItemProps = NodeRenderPropsWithChildren<ListItem>;

export type TopLevelProps =
	| TextProps
	| ParagraphProps
	| EmptyProps
	| ListItemProps;

export type AllProps = InlineProps | BlockProps | TopLevelProps;

export type RendererProps = {
	// inline
	bold: BoldProps;
	italic: ItalicProps;
	underline: UnderlineProps;
	strikethrough: StrikethroughProps;
	spoiler: SpoilerProps;
	emoji: EmojiProps;
	timestamp: TimestampProps;
	mention: MentionProps;
	link: LinkProps;
	code: CodeProps;
	code_block: CodeBlockProps;

	// block
	heading: HeadingProps;
	list: ListProps;
	quote: QuoteProps;
	small: SmallProps;

	// top-level
	text: TextProps;
	paragraph: ParagraphProps;
	empty: EmptyProps;

	// pseudo
	listItem: ListItemProps;
};

export type Renderers = {
	readonly [K in keyof RendererProps]?: React.FC<RendererProps[K]>;
};

export type NodeProps = {
	node: AnyNode;
	renderers: Renderers;
};

export type NodeListProps = {
	nodes: AnyNode[];
	renderers: Renderers;
};

export type MarkdownProps = {
	content: string;
	renderers: Renderers;
};

declare const RULES: Set<string>;

export function useAst(): Block[];
export function Node(props: NodeProps): React.ReactNode;
export function NodeList(props: NodeListProps): React.ReactNode;
export default function Markdown(props: MarkdownProps): React.ReactNode;
