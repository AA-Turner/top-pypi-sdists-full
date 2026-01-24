/**
 * @typedef {Object} SidePanel
 */

/**
 * @typedef {Object} PipecatBaseNode
 */

/**
 * @typedef {Object} FlowConfig
 * @property {string} initial_node
 * @property {Object.<string, NodeConfig>} nodes
 */

/**
 * @typedef {Object} NodeConfig
 * @property {Array<Message>} [role_messages] - Optional messages defining bot's role/personality
 * @property {Array<Message>} task_messages - Required messages defining the node's task
 * @property {Array<Function>} functions
 * @property {Array<Action>} [pre_actions]
 * @property {Array<Action>} [post_actions]
 */

/**
 * @typedef {Object} Message
 * @property {string} role
 * @property {string} content
 */

/**
 * @typedef {Object} Action
 * @property {string} type
 * @property {string} [text]
 */

/**
 * @typedef {Object} Function
 * @property {string} type
 * @property {FunctionDefinition} function
 */

/**
 * @typedef {Object} FunctionDefinition
 * @property {string} name
 * @property {string} description
 * @property {Object} parameters
 * @property {string} [transition_to]
 */
