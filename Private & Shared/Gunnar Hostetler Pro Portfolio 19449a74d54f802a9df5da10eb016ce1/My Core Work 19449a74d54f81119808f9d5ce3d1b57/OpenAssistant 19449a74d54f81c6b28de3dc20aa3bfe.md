# OpenAssistant

Industry: iOS Development
Key skills: Combine, REST, Swift, SwiftUI
Description: Native iOS App designed to interact with the OpenAI Assistants=v2 API
GitHub: https://github.com/Gunnarguy/OpenAssistant
App Store: https://apps.apple.com/us/app/openassistant/id6692613772

### **User-Facing Features (Current & Working)**

| Area | Key Interactions / Notes |
| --- | --- |
| **Assistant Management** | Create, view, edit and delete assistants; configure name, instructions, model (GPT-4o/4.1/O-series), temperature, top-p and reasoning effort. |
| **Tool Configuration** | Enable or disable tools (e.g., Code Interpreter, File Search) per assistant. |
| **Vector Store Operations** | Full CRUD on vector stores; associate stores with assistants; enable file-based retrieval. |
| **File Handling & Upload** | Upload PDF, TXT, DOCX and other formats; choose chunk size/overlap; manage metadata and association. |
| **Interactive Chat** | Real-time chat with assistants; Markdown rendering; persistent history; thread creation and lifecycle control. |
| **Reactive UI & Sync** | Combine + NotificationCenter used for asynchronous operations and decoupled updates across the app. |
| **API Key Persistence** | Stores the OpenAI API key securely via @AppStorage. |
| **Appearance & Theming** | Light, Dark and System themes selectable in settings. |
| **Native SwiftUI Experience** | Built entirely with SwiftUI and MVVM for a responsive, iOS-native feel. |

### **Screens / Flows (SwiftUI Views)**

**Flow Order:** Initial Setup → MainTabView (Assistants / Vector Stores / Chat / Settings)

- **Initial Setup** – Prompt for OpenAI API key via `SettingsView`; store securely.
- **AssistantsView** – Lists all assistants; create new assistant; tap to view details or delete.
- **AssistantDetailView** – Edit assistant properties (name, instructions, model, temperature, top-p), manage associated vector stores.
- **VectorStoreListView** – Lists vector stores; create new stores; tap to view details or delete.
- **VectorStoreDetailView** – View store details, file count, and list of files; add new files via `AddFileView`; delete files.
- **ChatView** – Select an assistant to initiate chat; send messages; view conversation and message history.
- **SettingsView** – Manage API key, adjust appearance, and other preferences.
- **CreateAssistantView** – Guided form to create assistants with configuration options.

### **Services & External Integrations**

| Service | Responsibility | External Source |
| --- | --- | --- |
| **APIService** | Central networking layer; manages requests, responses, authentication and retries. | OpenAI API |
| **OpenAIService-AssistantExt** | Assistant CRUD operations (fetch, create, update, delete). | OpenAI API |
| **OpenAIService-ThreadsExt** | Thread management: create threads, run assistants, send messages, poll run status. | OpenAI API |
| **OpenAIService-VectorExt** | Vector store operations: create, fetch, update, delete stores and files. | OpenAI API |
| **FileUploadService** | Handles multipart uploads of files to OpenAI and associates them with vector stores. | OpenAI API |
| **OpenAIInitializer** | Initializes and reinitializes the `APIService` with the provided API key. | Local |
| **MessageStore** | Persists chat messages in UserDefaults; provides Combine publishers for UI updates. | Local |
| **NotificationCenter** | Posts events for assistant updates, vector store changes and settings changes. | Local |
| **Combine** | Reactive framework for asynchronous data streams and state changes. | Local |

### **Data Models (Core Structs)**

| Model | Purpose | Notes |
| --- | --- | --- |
| **Assistant** | Represents an assistant entity with id, name, instructions, model, tools. | Mirrors OpenAI’s assistant definition. |
| **AssistantSettings** | Holds configuration: model, temperature, top-p, description, tools. | Used for creation and updates. |
| **Message** | Represents chat messages with role (user/assistant) and content. | Used for thread communication. |
| **Thread** | Defines chat context; contains messages and run identifiers. | Created per chat session. |
| **Run** | Represents an ongoing assistant run; includes status and completion info. | Polling monitors state until completion. |
| **VectorStore** | Holds metadata for a vector store (id, name, description, file count). | Used to group documents for retrieval. |
| **VectorStoreFile** | Describes a file uploaded to a vector store; includes id, bytes, metadata. | Supports deletion and detail display. |

### **ViewModels (ObservableObjects)**

| ViewModel | Drives | Emits |
| --- | --- | --- |
| **ContentViewModel** | Root state: API key check, loading. | isLoading, selectedAssistant. |
| **AssistantManagerViewModel** | Fetch/create/update/delete assistants; manages model list and vector store associations. | assistants, availableModels, error messages. |
| **AssistantDetailViewModel** | Edit assistant settings, manage vector store association. | Assistant state, update statuses. |
| **AssistantPickerViewModel** | List assistants for chat selection. | assistants, isLoading, errors. |
| **ChatViewModel** | Thread lifecycle: create thread, add messages, run assistant, poll run status. | messages, isLoading, progress. |
| **VectorStoreManagerViewModel** | Vector store CRUD; file upload and deletion. | vectorStores, files, progress. |

### **Processing Pipeline (Step-by-Step)**

Although OpenAssistant does not embed text like a RAG system, it orchestrates the lifecycle of assistants, files and chat sessions:

1. **Setup** – User enters OpenAI API key; `OpenAIInitializer` configures `APIService`.
2. **Assistant Creation** – In `AssistantManagerView`, user fills out `CreateAssistantView` with name, instructions, model, temperature, top-p and enabled tools; the app calls `OpenAIService-AssistantExt` to create the assistant.
3. **Vector Store Management** – User creates a vector store; associate one or more stores with an assistant.
4. **File Upload** – Through `AddFileView`, user selects files; each file is chunked per user settings (chunk size/overlap) and uploaded via `FileUploadService` to the selected vector store; metadata is stored with the store.
5. **Assistant Update** – After associating files, user can modify assistant settings (e.g., switch models, adjust temperature) via `AssistantDetailViewModel`.
6. **Chat Initiation** – Selecting an assistant in `ChatView` triggers creation of a thread (`OpenAIService-ThreadsExt`).
7. **Run Assistant** – User sends a message; the app calls `createRun` and begins polling run status at intervals using a timer (`ChatViewModel`), updating progress.
8. **Receive Response** – Once the run completes, messages are appended to `MessageStore`; UI updates with the new assistant reply.
9. **Persist & Notify** – Chat history is persisted; `NotificationCenter` posts events for other views to refresh (e.g., updated assistant or vector store state).

### **Concurrency & Reactive Pieces**

- **`async/await`** – All API calls and file operations use Swift’s structured concurrency; e.g., uploading multiple files concurrently via `TaskGroup`.
- **Combine** – ViewModels expose `@Published` properties; views automatically update in response. Polling for run status is scheduled via Combine timers.
- **Decoupled Updates** – `NotificationCenter` broadcasts changes (assistant created, updated, or deleted) so lists refresh without tight coupling.
- **Error Handling & Retry** – The `APIService` includes logic for retrying failed requests with exponential backoff; errors propagate through view models.

### **Persistence & Security**

| Item | Mechanism | Note |
| --- | --- | --- |
| **API Key Storage** | `@AppStorage` in SwiftUI | Persists across launches; value stored in UserDefaults. |
| **Chat History** | `MessageStore` | Saves messages in JSON format to UserDefaults. |
| **Assistant & Store Lists** | In-memory (refreshed via API) | Persisted server-side on OpenAI; refreshed at launch. |
| **Error & Progress Logs** | In-memory | Displayed via alerts and progress views; not persisted. |
| **Secure Networking** | HTTPS & bearer tokens | All API calls use HTTPS with API key authorization. |

### **UI & Design System**

- **SwiftUI Components** – Uses stacks, lists and forms; custom views for chat bubbles, loading indicators and forms.
- **Theming** – Supports Light, Dark and System modes; accent colors adapt accordingly.
- **Navigation** – `MainTabView` provides tab bar navigation; navigation links present detail views.
- **Accessibility** – Leverages SwiftUI’s accessibility modifiers; improvements planned to enhance VoiceOver support.

### **Diagnostics & Telemetry**

- **Error Publishing** – ViewModels publish error messages via `@Published`, triggering alerts in the UI.
- **Progress Indicators** – File uploads and run polling display progress bars or spinning indicators.
- **Debug Logging** – Standard `print` statements and Combine subscribers used during development; no central log persistence.

### **Build & Deployment**

- **Architecture** – Pure SwiftUI with MVVM; the codebase is modularly organized into API services, view models, views and utilities.
- **Project** – Xcode project file (`OpenAssistant.xcodeproj`) organizes targets and build settings.
- **Distribution** – Built for iOS; distribution via TestFlight/App Store is not specified but supported.
- **Configuration** – Uses Debug and Release `.xcconfig` files to control build settings (e.g., strict concurrency flags).

### **Known Gaps / TODO (Current)**

- **Error Handling** – Improve robustness across API interactions and data persistence.
- **Unit Testing** – Increase coverage for view models and services.
- **Performance Optimization** – Optimize data fetching, state updates and UI rendering.
- **Accessibility** – Enhance accessibility to support a wider range of users.

### **Planned Features / Backlog**

- [ ]  Expand error handling with user-friendly retry prompts and offline fallback.
- [ ]  Add integration tests for assistant and chat flows.
- [ ]  Implement performance profiling and caching to reduce latency.
- [ ]  Improve accessibility: provide VoiceOver labels for custom controls, support Dynamic Type.
- [ ]  Support additional OpenAI models or capabilities when available.
- [ ]  Provide a dark/light theme preview in settings.

### **At-a-Glance Metrics**

| Metric | Value |
| --- | --- |
| **Total Lines of Code (LOC)** | ~10,137 (approx.) |
| **Swift LOC** | ~8,489 (≈83.8% of repo) |
| **Documentation & Config LOC** | ~1,648 (≈16.2% of repo) |
| **MVVM Feature Modules** | 7 (`Bases`, `Assistants`, `Chat`, `VectorStores`, `Settings`, `Content`, `Main`) |
| **Primary SwiftUI Views** | 8 (`ContentView`, `AssistantManagerView`, `AssistantDetailView`, `AssistantPickerView`, `VectorStoreListView`, `VectorStoreDetailView`, `ChatView`, `SettingsView`) |
| **Service Layer Components** | 5 (`APIService` and its Assistant/Thread/Vector extensions, `FileUploadService`) |
| **External APIs** | 1 (OpenAI API) |
| **Processing Pipeline Steps** | 9 distinct stages in the assistant/vector/chat lifecycle |
| **Concurrency Models** | 3 (`async/await`, Combine, Timer-based polling) |
| **Supported File Types** | Multiple (PDF, TXT, DOCX, others via file upload) |
| **Available Themes** | 3 (Light, Dark, System) |