typedef enum NodeIteratorState {
  MaybeMore,
  Consumed,
} NodeIteratorState;

typedef enum NodeResultType {
  String,
  Enum,
  Int,
  Float,
  Bool,
  Object,
  Void,
  Unknown,
} NodeResultType;

typedef struct SizedString {
  uint8_t bytes[255];
  uint8_t length;
} SizedString;

typedef struct NodeResult {
  uint32_t id;
  bool error;
  enum NodeResultType type;
  struct SizedString object_type_name;
  struct SizedString enum_value;
} NodeResult;

typedef struct NodeIteratorResult {
  uint32_t id;
  bool error;
} NodeIteratorResult;

typedef struct NodeIteratorNextResult {
  enum NodeIteratorState state;
  bool error;
  struct NodeResult node;
} NodeIteratorNextResult;

typedef struct EvaluateResult {
  bool error;
  const uint8_t *value;
  uintptr_t length;
} EvaluateResult;

/**
 * # Safety
 *
 * This is unsafe because we accept raw pointers to strings. Callers must
 * ensure they pass in proper NULL terminated C strings.
 */
struct NodeResult create(const char *variable_values,
                         const char *fallback_init_data,
                         const char *token,
                         const char *init_query,
                         const char *query,
                         const char *options);

void node_close(uint32_t node_handle);

void node_flush_logs(uint32_t node_handle);

/**
 * # Safety
 *
 * This is unsafe because we accept raw pointers to strings. Callers must
 * ensure they pass in proper NULL terminated C strings.
 */
struct NodeResult node_get_field(uint32_t node_handle, const char *field, const char *arguments);

struct NodeIteratorResult node_get_items(uint32_t node_handle);

struct NodeIteratorNextResult node_iterator_next(uint32_t iterator_handle);

struct EvaluateResult node_evaluate(uint32_t node_handle);

void node_free(uint32_t node_handle);

void node_log_unexpected_type_error(uint32_t node_handle);

void node_log_unexpected_value_error(uint32_t node_handle);

void wait_for_initialization(uint32_t node_handle);
