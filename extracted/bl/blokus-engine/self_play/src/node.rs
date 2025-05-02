// Game Tree to be used by each MCTS simulation
use std::collections::HashMap;


/// Each node in the game tree represents a state of the game
/// There is one state for every tile placement
#[derive(Clone)]
pub struct Node {
    pub children: HashMap<usize, Node>,
    pub to_play: usize,
    pub value_sum: f32,
    pub visits: u32,
    pub prior: f32,
}

impl Node {
    pub fn new(prior: f32) -> Node {
        Node {
            children: HashMap::new(),
            to_play: 0,
            value_sum: 0.0,
            visits: 0,
            prior: prior,
        }
    }   

    /// Has the node been explored before
    pub fn is_expanded(&self) -> bool {
        self.children.len() > 0
    }

    /// Get the value of the node
    pub fn value(&self) -> f32 {
        if self.visits == 0 {
            0.0
        } else {
            self.value_sum / self.visits as f32
        }
    }

}
