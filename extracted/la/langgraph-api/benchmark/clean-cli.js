import { clean } from './clean.js';

clean().catch(error => {
    console.error('Unhandled error:', error.message);
    process.exit(1);
});
