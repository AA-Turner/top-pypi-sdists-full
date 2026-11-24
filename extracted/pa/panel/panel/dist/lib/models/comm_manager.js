import { ModelChangedEvent } from "@bokehjs/document";
import { View } from "@bokehjs/core/view";
import { Model } from "@bokehjs/model";
import { Message } from "@bokehjs/protocol/message";
import { Receiver } from "@bokehjs/protocol/receiver";
import { Buffer } from "@bokehjs/core/serialization/buffer";
import { isArray, isPlainObject } from "@bokehjs/core/util/types";
import { keys } from "@bokehjs/core/util/object";
export const comm_settings = {
    debounce: true,
};
export class CommManagerView extends View {
}
export class CommManager extends Model {
    ns;
    _receiver;
    _client_comm;
    _event_buffer;
    _timeout;
    _blocked;
    _reconnect;
    constructor(attrs) {
        super(attrs);
    }
    initialize() {
        super.initialize();
        this._receiver = new Receiver();
        this._event_buffer = [];
        this._blocked = false;
        this._reconnect = false;
        this._timeout = Date.now();
        if ((window.PyViz == undefined) || (!window.PyViz.comm_manager)) {
            console.warn("Could not find comm manager on window.PyViz, ensure the extension is loaded.");
        }
        else {
            this.ns = window.PyViz;
            this.ns.comm_manager.register_target(this.plot_id, this.comm_id, (msg) => {
                for (const view of this.ns.shared_views.get(this.plot_id) ?? []) {
                    if (view !== this) {
                        try {
                            view.msg_handler(msg);
                        }
                        catch (e) {
                            console.error(e);
                        }
                    }
                }
                try {
                    this.msg_handler(msg);
                }
                catch (e) {
                    console.error(e);
                }
            });
            this._client_comm = this.ns.comm_manager.get_client_comm(this.plot_id, this.client_comm_id, (msg) => {
                // Views of the same plot share one client comm and only the view
                // that opened it receives the acknowledgements
                for (const view of this.ns.shared_views.get(this.plot_id) ?? []) {
                    if (view !== this) {
                        try {
                            view._unblock();
                        }
                        catch (e) {
                            console.error(e);
                        }
                    }
                }
                this.on_ack(msg);
            });
            this._reconnect = !this._client_comm?.active || false;
            this._register_view();
        }
    }
    _register_view() {
        if (this.ns == null) {
            return;
        }
        if (this.ns.shared_views == null) {
            this.ns.shared_views = new Map();
        }
        const views = this.ns.shared_views.get(this.plot_id);
        if (views == null) {
            this.ns.shared_views.set(this.plot_id, [this]);
        }
        else if (!views.includes(this)) {
            views.push(this);
        }
    }
    _unregister_view() {
        this.document?.remove_on_change(this._document_listener);
        const views = this.ns?.shared_views?.get(this.plot_id);
        if (views == null) {
            return;
        }
        const remaining = views.filter((view) => view !== this);
        if (remaining.length) {
            this.ns.shared_views.set(this.plot_id, remaining);
        }
        else {
            this.ns.shared_views.delete(this.plot_id);
        }
    }
    _document_listener = (event) => this._document_changed(event);
    _doc_attached() {
        super._doc_attached();
        if (this.document != null) {
            this.document.on_change(this._document_listener);
        }
        this._register_view();
    }
    // Notebook outputs are cleared rather than destroyed, so a disposed view
    // is only ever detached from its document
    _doc_detached() {
        this._unregister_view();
        super._doc_detached();
    }
    _document_changed(event) {
        // Changes applied from a Python patch are not synced; echoing them back
        // would also resend models Python already knows as new models
        if (!event.sync) {
            return;
        }
        // Filter out changes to attributes that aren't server-visible
        if (event instanceof ModelChangedEvent && !event.model.properties[event.attr].syncable) {
            return;
        }
        this._event_buffer.push(event);
        if (this._reconnect && this._client_comm?.connected) {
            this.on_ack({ metadata: { msg_type: "Ready" } });
        }
        else if (!comm_settings.debounce) {
            this.process_events();
        }
        else if ((!this._blocked || (Date.now() > this._timeout))) {
            setTimeout(() => this.process_events(), this.debounce);
            this._blocked = true;
            this._timeout = Date.now() + this.timeout;
        }
    }
    _extract_buffers(value, buffers) {
        if (isArray(value)) {
            for (const val of value) {
                this._extract_buffers(val, buffers);
            }
        }
        else if (value instanceof Map) {
            for (const key of value.keys()) {
                const v = value.get(key);
                this._extract_buffers(v, buffers);
            }
        }
        else if (value instanceof Buffer) {
            const { buffer } = value;
            const id = buffers.length;
            buffers.push(buffer);
            return { id };
        }
        else if (isPlainObject(value)) {
            for (const key of keys(value)) {
                const replaced = this._extract_buffers(value[key], buffers);
                if (replaced != null) {
                    value[key] = replaced;
                }
            }
        }
    }
    process_events() {
        if ((this.document == null) || (this._client_comm == null)) {
            return;
        }
        if (this._event_buffer.length === 0) {
            return;
        }
        const patch = this.document.create_json_patch(this._event_buffer);
        this._event_buffer = [];
        const message = { ...Message.create("PATCH-DOC", {}, patch) };
        const buffers = [];
        this._extract_buffers(message.content, buffers);
        this._client_comm.send(message, {}, buffers);
        for (const view of this.ns.shared_views.get(this.plot_id) ?? []) {
            if (view !== this && view.document != null) {
                view.document.apply_json_patch(patch, [], this.id);
            }
        }
    }
    disconnect_signals() {
        super.disconnect_signals();
        this._unregister_view();
    }
    _unblock() {
        if (this._event_buffer.length > 0) {
            this._blocked = true;
            this._timeout = Date.now() + this.timeout;
            this.process_events();
        }
        else {
            this._blocked = false;
        }
    }
    on_ack(msg) {
        // Receives acknowledgement from Python, processing event
        // and unblocking Comm if event queue empty
        const metadata = msg.metadata;
        this._unblock();
        if ((metadata.msg_type == "Ready") && metadata.content) {
            // eslint-disable-next-line no-console
            console.log("Python callback returned following output:", metadata.content);
        }
        else if (metadata.msg_type == "Error") {
            console.warn("Python failed with the following traceback:", metadata.traceback);
        }
    }
    msg_handler(msg) {
        const metadata = msg.metadata;
        const buffers = msg.buffers;
        const content = msg.content.data;
        const plot_id = this.plot_id;
        if ((metadata.msg_type == "Ready")) {
            if (metadata.content) {
                // eslint-disable-next-line no-console
                console.log("Python callback returned following output:", metadata.content);
            }
            else if (metadata.msg_type == "Error") {
                console.warn("Python failed with the following traceback:", metadata.traceback);
            }
        }
        else if (plot_id != null) {
            let plot = null;
            if ((plot_id in this.ns.plot_index) && (this.ns.plot_index[plot_id] != null)) {
                plot = this.ns.plot_index[plot_id];
            }
            else if ((window.Bokeh !== undefined) && (plot_id in window.Bokeh.index)) {
                plot = window.Bokeh.index[plot_id];
            }
            if (plot == null) {
                return;
            }
            if (content.length) {
                this._receiver.consume(content);
            }
            else if ((buffers != undefined) && (buffers.length > 0)) {
                this._receiver.consume(buffers[0].buffer);
            }
            else {
                return;
            }
            const comm_msg = this._receiver.message;
            if ((comm_msg != null) && (Object.keys(comm_msg.content).length > 0) && this.document != null) {
                const patch = comm_msg.content;
                this.document.apply_json_patch(patch, comm_msg.buffers);
            }
        }
    }
    static __module__ = "panel.models.comm_manager";
    static {
        this.prototype.default_view = CommManagerView;
        this.define(({ Int, Str, Nullable }) => ({
            plot_id: [Nullable(Str), null],
            comm_id: [Nullable(Str), null],
            client_comm_id: [Nullable(Str), null],
            timeout: [Int, 5000],
            debounce: [Int, 50],
        }));
    }
}
//# sourceMappingURL=comm_manager.js.map