struct dcp_press;
struct dcp_scan;
struct dcp_batch;

// Press
struct dcp_press *dcp_press_new(void);
int               dcp_press_setup(struct dcp_press *, int gencode_id, float epsilon);
int               dcp_press_open(struct dcp_press *, char const *hmm, char const *db);
long              dcp_press_nproteins(struct dcp_press const *);
int               dcp_press_next(struct dcp_press *);
bool              dcp_press_end(struct dcp_press const *);
int               dcp_press_close(struct dcp_press *);
void              dcp_press_del(struct dcp_press const *);

// Scan
struct dcp_scan *dcp_scan_new(void);
void             dcp_scan_del(struct dcp_scan const *);
int              dcp_scan_setup(struct dcp_scan *, char const *dbfile, int port,
                                int num_threads, bool multi_hits, bool hmmer3_compat,
                                bool cache, void (*callback)(void *), void *userdata);
int              dcp_scan_run(struct dcp_scan *, struct dcp_batch *, char const *product_dir);
void             dcp_scan_interrupt(struct dcp_scan *);
int              dcp_scan_progress(struct dcp_scan const *);

// Batch
struct dcp_batch *dcp_batch_new(void);
void              dcp_batch_del(struct dcp_batch *);
int               dcp_batch_add(struct dcp_batch *, long id, char const *name, char const *data);
void              dcp_batch_reset(struct dcp_batch *);


// Strerror
char const *dcp_error_string(int error_code);

// Stdio
FILE *fopen(char const *filename, char const *mode);
FILE *fdopen(int, char const *);
int   fclose(FILE *);

extern "Python" void callback(void *);
