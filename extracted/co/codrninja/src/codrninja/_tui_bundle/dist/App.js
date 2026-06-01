import React, { useCallback, useEffect, useRef, useState } from 'react';
import { Box, Text } from 'ink';
import { createSession, deleteSession, fetchConfig, fetchProviders, fetchSession, fetchSessions, fetchVersion } from './api.js';
import { SessionList } from './SessionList.js';
import { ChatView } from './ChatView.js';
import { ModelSelect } from './ModelSelect.js';
import { ProviderSelect } from './ProviderSelect.js';
import { ProviderConfig } from './ProviderConfig.js';
export function App() {
    const [screen, setScreen] = useState('sessions');
    const [sessions, setSessions] = useState([]);
    const [activeName, setActiveName] = useState(null);
    const [history, setHistory] = useState([]);
    const [config, setConfig] = useState({});
    const [prevScreen, setPrevScreen] = useState('sessions');
    const [configProvider, setConfigProvider] = useState(null);
    const [loadError, setLoadError] = useState('');
    const [loading, setLoading] = useState(true);
    const [sessionModel, setSessionModelState] = useState('');
    const [sessionProvider, setSessionProviderState] = useState('');
    const [providers, setProviders] = useState([]);
    const [version, setVersion] = useState('');
    // stable ref so openSession callback doesn't need sessions in its deps
    const sessionsRef = useRef([]);
    useEffect(() => { sessionsRef.current = sessions; }, [sessions]);
    const openSession = useCallback(async (name) => {
        try {
            const data = await fetchSession(name);
            const msgs = (data.messages ?? [])
                .filter((m) => m.role === 'user' || m.role === 'assistant')
                .map((m) => ({ role: m.role, content: m.content }));
            const s = sessionsRef.current.find((x) => x.name === name);
            setSessionModelState(s?.model ?? '');
            setSessionProviderState(s?.provider ?? '');
            setHistory(msgs);
            setActiveName(name);
            setScreen('chat');
        }
        catch {
            setHistory([]);
            setActiveName(name);
            setScreen('chat');
        }
    }, []);
    useEffect(() => {
        async function init() {
            try {
                const [cfg, sess, provs, ver] = await Promise.all([
                    fetchConfig(), fetchSessions(), fetchProviders(), fetchVersion(),
                ]);
                setProviders(provs.providers ?? []);
                setVersion(ver);
                setConfig(cfg);
                setSessions(sess);
                const autoSession = process.env['CODRNINJA_SESSION'];
                if (autoSession) {
                    const exists = sess.find((s) => s.name === autoSession);
                    if (!exists)
                        await createSession(autoSession);
                    await openSession(autoSession);
                    return;
                }
            }
            catch (e) {
                setLoadError(`Cannot reach server. Start it with: codrninja serve\n  ${String(e)}`);
            }
            finally {
                setLoading(false);
            }
        }
        void init();
    }, [openSession]);
    async function newSession(name) {
        try {
            await createSession(name);
            const sess = await fetchSessions();
            setSessions(sess);
            await openSession(name);
        }
        catch (e) {
            setLoadError(String(e));
        }
    }
    function backToSessions() {
        setScreen('sessions');
        fetchSessions().then(setSessions).catch(() => { });
    }
    async function handleDeleteSession(name) {
        try {
            await deleteSession(name);
            const sess = await fetchSessions();
            setSessions(sess);
        }
        catch { /* ignore */ }
    }
    function openModelSelect() {
        setPrevScreen(screen);
        setScreen('model-select');
    }
    function onModelSelected(model, provider) {
        if (prevScreen === 'chat' && activeName) {
            // Re-open session so ChatView remounts with full backend history
            setSessionModelState(model);
            setSessionProviderState(provider);
            void openSession(activeName);
        }
        else {
            setConfig((c) => ({ ...c, model, provider }));
            setScreen(prevScreen);
        }
    }
    function openProviderSelect() {
        setPrevScreen(screen);
        setScreen('provider-select');
    }
    function onProviderChosen(p) {
        setConfigProvider(p);
        setScreen('provider-config');
    }
    function onProviderConfigDone(newProvider, newModel) {
        setConfig((c) => ({
            ...c,
            provider: newProvider,
            ...(newModel ? { model: newModel } : {}),
        }));
        if (prevScreen === 'chat' && activeName) {
            void openSession(activeName);
        }
        else {
            setScreen(prevScreen);
        }
    }
    if (loading) {
        return (React.createElement(Box, { paddingX: 2 },
            React.createElement(Text, { dimColor: true }, "Connecting to server\u2026")));
    }
    if (loadError) {
        return (React.createElement(Box, { flexDirection: "column", paddingX: 2 },
            React.createElement(Text, { bold: true, color: "red" }, "Error"),
            React.createElement(Text, null, loadError)));
    }
    if (screen === 'provider-select') {
        return (React.createElement(ProviderSelect, { onSelect: onProviderChosen, onCancel: () => setScreen(prevScreen) }));
    }
    if (screen === 'provider-config' && configProvider) {
        return (React.createElement(ProviderConfig, { provider: configProvider, onDone: onProviderConfigDone, onCancel: () => setScreen(prevScreen) }));
    }
    if (screen === 'model-select') {
        const fromChat = prevScreen === 'chat';
        return (React.createElement(ModelSelect, { currentModel: fromChat ? (sessionModel || (config['model'] ?? '')) : (config['model'] ?? ''), currentProvider: fromChat ? (sessionProvider || (config['provider'] ?? '')) : (config['provider'] ?? ''), sessionName: fromChat && activeName ? activeName : undefined, onSelect: onModelSelected, onCancel: () => setScreen(prevScreen) }));
    }
    if (screen === 'chat' && activeName) {
        return (React.createElement(ChatView, { sessionName: activeName, history: history, onBack: backToSessions, onOpenModelSelect: openModelSelect, onOpenProviderSelect: openProviderSelect, provider: sessionProvider || (config['provider'] ?? ''), model: sessionModel || (config['model'] ?? '') }));
    }
    return (React.createElement(SessionList, { sessions: sessions, onSelect: openSession, onNew: newSession, onDelete: handleDeleteSession, error: loadError, version: version, providers: providers }));
}
