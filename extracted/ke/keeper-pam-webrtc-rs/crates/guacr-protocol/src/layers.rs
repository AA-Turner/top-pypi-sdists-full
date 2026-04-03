// Layer management instruction formatting for Guacamole protocol
//
// Supports: dispose, move

use crate::format_instruction;

/// Format `dispose` instruction - Dispose/destroy layer
///
/// Format: `6.dispose,{layer};`
///
/// # Arguments
/// - `layer`: Layer index to dispose
pub fn format_dispose(layer: i32) -> String {
    let layer_str = layer.to_string();
    format_instruction("dispose", &[&layer_str])
}

/// Format `move` instruction - Move layer
///
/// Format: `4.move,{layer},{parent},{x},{y},{z};`
///
/// # Arguments
/// - `layer`: Layer index to move
/// - `parent`: Parent layer index (or -1 for default)
/// - `x`: New X coordinate
/// - `y`: New Y coordinate
/// - `z`: Z-order (stacking order)
pub fn format_move(layer: i32, parent: i32, x: u32, y: u32, z: i32) -> String {
    let layer_str = layer.to_string();
    let parent_str = parent.to_string();
    let x_str = x.to_string();
    let y_str = y.to_string();
    let z_str = z.to_string();

    format_instruction("move", &[&layer_str, &parent_str, &x_str, &y_str, &z_str])
}

/// Format `size` instruction - Set layer size
///
/// Format: `4.size,{layer},{width},{height};`
///
/// # Arguments
/// - `layer`: Layer index
/// - `width`: Layer width in pixels
/// - `height`: Layer height in pixels
pub fn format_size(layer: i32, width: u32, height: u32) -> String {
    let layer_str = layer.to_string();
    let width_str = width.to_string();
    let height_str = height.to_string();

    format_instruction("size", &[&layer_str, &width_str, &height_str])
}
