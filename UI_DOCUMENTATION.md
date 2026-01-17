# UI Documentation - Universal Repository Setup Wizard

## Application Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Universal Repository Setup Wizard                         [_][□][X]│
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                  Repository Setup Wizard                        │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ 1. Select Repository Source                              │  │
│  │                                                           │  │
│  │  ○ Local Folder   ○ ZIP File   ○ Git URL                │  │
│  │                                                           │  │
│  │  Source: [________________________________] [Browse...]   │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ 2. Select Target Directory                               │  │
│  │                                                           │  │
│  │  Target: [________________________________] [Browse...]   │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ 3. Setup Options                                         │  │
│  │                                                           │  │
│  │  ☑ Automatically install dependencies                    │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ Progress                                                  │  │
│  │                                                           │  │
│  │  [████████████████████░░░░░░░░░░░░░░░░░░░░░░░]           │  │
│  │                                                           │  │
│  │  ┌───────────────────────────────────────────────────┐  │  │
│  │  │ [18:52:24] INFO: Starting repository setup...     │  │  │
│  │  │ [18:52:25] INFO: Target directory: ~/repo_setups  │  │  │
│  │  │ [18:52:26] INFO: Cloning from URL...              │  │  │
│  │  │ [18:52:30] INFO: Clone completed successfully     │  │  │
│  │  │ [18:52:31] INFO: Checking for dependencies...     │  │  │
│  │  │ [18:52:32] SUCCESS: Setup completed!              │  │  │
│  │  └───────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│              [Start Setup] [Clear Log] [Exit]                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## UI Components Description

### 1. Title Bar
- **Application Name**: "Universal Repository Setup Wizard"
- **Standard window controls**: Minimize, Maximize, Close

### 2. Main Title
- Large, bold text: "Repository Setup Wizard"
- Centered at the top of the window

### 3. Source Selection Section
**Purpose**: Choose where the repository comes from

**Components**:
- **Radio Buttons** (3 options):
  - ○ Local Folder
  - ○ ZIP File  
  - ○ Git URL
  
- **Source Entry Field**:
  - Text input for path or URL
  - Width: Expands with window
  
- **Browse Button**:
  - Opens file/folder browser
  - Disabled for Git URL option

### 4. Target Directory Section
**Purpose**: Choose where to install the repository

**Components**:
- **Target Entry Field**:
  - Pre-filled with default: `~/repo_setups`
  - Text input for destination path
  
- **Browse Button**:
  - Opens folder browser
  - Always enabled

### 5. Setup Options Section
**Purpose**: Configure setup behavior

**Components**:
- **Checkbox**: "Automatically install dependencies"
  - Default: Checked (enabled)
  - Controls whether to auto-install from requirements.txt, package.json, etc.

### 6. Progress Section
**Purpose**: Real-time feedback during setup

**Components**:
- **Progress Bar**:
  - Indeterminate mode (animated)
  - Shows activity during processing
  
- **Log Display**:
  - Scrollable text area
  - Monospace font (Courier)
  - Timestamped messages
  - Color-coded by level (INFO, WARNING, ERROR, SUCCESS)
  - Auto-scrolls to newest messages
  - Height: Expands with window

### 7. Action Buttons
**Purpose**: Control the wizard

**Components**:
- **Start Setup** (Primary action):
  - Styled as accent button (bold)
  - Disabled while processing
  - Validates inputs before starting
  
- **Clear Log**:
  - Clears the log display
  - Always enabled
  
- **Exit**:
  - Closes the application
  - Confirms if setup is in progress

## Color Scheme

### Standard Colors (Theme: Clam/Alt)
- **Background**: Light gray (#E0E0E0)
- **Text**: Dark gray (#000000)
- **Button**: Light blue (#D0D0FF)
- **Selection**: Blue (#4A90D9)
- **Progress Bar**: Blue animated

### Log Level Colors (Conceptual)
- **INFO**: Default text color
- **SUCCESS**: Green (in message text)
- **WARNING**: Orange (in message text)
- **ERROR**: Red (in message text)

## Responsive Design

### Window Sizing
- **Default Size**: 800x600 pixels
- **Minimum Size**: 700x500 pixels
- **Resizable**: Yes
- **Centered**: On screen at launch

### Layout Behavior
- All sections expand horizontally with window
- Log display expands both horizontally and vertically
- Buttons remain at bottom
- Sections maintain fixed vertical spacing

## User Interaction Flow

### Typical Workflow
```
1. Launch Application
   ↓
2. Select Source Type (Radio Button)
   ↓
3. Enter/Browse Source (Text Field + Button)
   ↓
4. Confirm/Modify Target (Text Field + Button)
   ↓
5. Configure Options (Checkbox)
   ↓
6. Click "Start Setup" (Button)
   ↓
7. Monitor Progress (Progress Bar + Log)
   ↓
8. Completion (Dialog Box + Log Message)
```

### Error Workflow
```
1. Invalid Input Detected
   ↓
2. Show Error Dialog
   ↓
3. User Corrects Input
   ↓
4. Retry "Start Setup"
```

## Accessibility Features

### Keyboard Navigation
- **Tab**: Move between fields
- **Space**: Toggle checkboxes/radio buttons
- **Enter**: Activate focused button
- **Arrow Keys**: Navigate radio buttons

### Visual Feedback
- Button state changes (enabled/disabled)
- Progress bar animation
- Real-time log updates
- Dialog boxes for confirmations and errors

## State Management

### Application States

**Idle State**:
- Start Setup: Enabled
- All inputs: Enabled
- Progress bar: Hidden/Stopped

**Processing State**:
- Start Setup: Disabled
- All inputs: Enabled (can view)
- Progress bar: Animated
- Log: Updating

**Error State**:
- Error dialog displayed
- User can review and retry

**Complete State**:
- Success dialog displayed
- All inputs: Re-enabled
- Progress bar: Stopped
- Start Setup: Enabled

## Dialog Boxes

### Success Dialog
```
┌────────────────────────────────┐
│  Success                    [X]│
├────────────────────────────────┤
│  Repository setup completed!   │
│                                │
│  Location:                     │
│  /home/user/repo_setups/repo   │
│                                │
│          [   OK   ]            │
└────────────────────────────────┘
```

### Error Dialog
```
┌────────────────────────────────┐
│  Error                      [X]│
├────────────────────────────────┤
│  Setup failed:                 │
│  Source folder does not exist  │
│                                │
│          [   OK   ]            │
└────────────────────────────────┘
```

### Confirmation Dialog
```
┌────────────────────────────────┐
│  Confirm Exit               [X]│
├────────────────────────────────┤
│  Setup is in progress.         │
│  Are you sure you want to exit?│
│                                │
│      [  Yes  ]  [  No  ]       │
└────────────────────────────────┘
```

## Best Practices Implementation

### Usability
- Clear labels and descriptions
- Logical tab order
- Immediate visual feedback
- Informative error messages
- Default values for convenience

### Performance
- Non-blocking UI (threaded operations)
- Responsive during long operations
- Efficient file operations
- Resource cleanup

### Reliability
- Input validation before processing
- Graceful error handling
- Comprehensive logging
- Safe exit procedures

## Future UI Enhancements

### Potential Additions
- Dark mode toggle
- Custom color themes
- Font size adjustment
- Advanced options panel
- History of recent setups
- Favorites/bookmarks
- Multi-repository queue
- Drag-and-drop support

---

**UI Framework**: tkinter (Python standard library)  
**Design Philosophy**: Simple, clean, production-ready  
**Target Users**: Developers of all skill levels
