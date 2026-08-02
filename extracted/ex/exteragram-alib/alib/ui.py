from typing import Any, List, Optional

from alib import State

try:
    from extera_utils.classes import Base, java_subclass, joverride
    from org.telegram.ui.Cells import TextCell
    from android.widget import FrameLayout
    from java import jint, jboolean
    has_android = True
    try:
        from org.telegram.ui.Cells import SlideIntChooseView
        has_slide_view = True
    except ImportError:
        has_slide_view = False
        class SlideIntChooseView:
            pass
except ImportError:
    has_android = False
    has_slide_view = False

    class Base:
        @classmethod
        def new_java_instance(cls, *args, **kwargs):
            return cls()
        @classmethod
        def new_instance(cls, *args, **kwargs):
            return cls()

    def java_subclass(*args, **kwargs):
        return lambda cls: cls

    def joverride(*args, **kwargs):
        return lambda func: func

    def jint(val): return val

    def jboolean(val): return val

    class MockTextView:
        def getVisibility(self): return 0
        def getMeasuredWidth(self): return 100
        def getMeasuredHeight(self): return 20
        def measure(self, w, h): pass
        def getLeft(self): return 71
        def getRight(self): return 300
        def layout(self, l, t, r, b): pass

    class MockImageView:
        def getVisibility(self): return 8

    class TextCell:
        def __init__(self):
            self.textView = MockTextView()
            self.valueTextView = MockTextView()
            self.imageView = MockImageView()
            self.subtitleView = MockTextView()
            self.leftPadding = 23
            self.offsetFromImage = 71
            self.imageLeft = 21
            self.heightDp = 50
        def setEnabled(self, enabled): pass
        def onMeasure(self, w, h): pass
        def onLayout(self, c, l, t, r, b): pass
        def setSubtitle(self, text): pass
        def getCheckBox(self): return None

    class SlideIntChooseView:
        def setEnabled(self, enabled): pass

    class FrameLayout:
        def setEnabled(self, enabled): pass

def _get_subtitle_view(cell):

    try:

        field = cell.getClass().getSuperclass().getDeclaredField("subtitleView")

        field.setAccessible(True)

        return field.get(cell)

    except Exception:

        return getattr(cell, "subtitleView", None)

@java_subclass(TextCell)

class EnabledTextCell(Base):

    @joverride()

    def setEnabled(self, enabled):

        super().setEnabled(True)

    @joverride()

    def onMeasure(self, widthMeasureSpec: int, heightMeasureSpec: int):

        super().onMeasure(widthMeasureSpec, heightMeasureSpec)

        try:

            sub = _get_subtitle_view(self)

            sub_text = sub.getText() if sub is not None else None

            has_subtitle = sub is not None and sub.getVisibility() == 0 and sub_text is not None and str(sub_text).strip() != ""

            if not has_subtitle:

                return

            from android.view import View

            from org.telegram.messenger import AndroidUtilities

            width = View.MeasureSpec.getSize(widthMeasureSpec)

            image_view = self.imageView

            has_icon = image_view is not None and image_view.getVisibility() == 0

            left_offset = AndroidUtilities.dp(self.offsetFromImage if has_icon else self.leftPadding)

            check_box = self.getCheckBox()

            has_switch = check_box is not None and check_box.getVisibility() == 0

            value_text_view = self.valueTextView

            has_value_text = value_text_view is not None and value_text_view.getVisibility() == 0

            if has_switch:

                right_reserve = AndroidUtilities.dp(75)

            elif has_value_text:

                right_reserve = value_text_view.getMeasuredWidth() + AndroidUtilities.dp(16)

            else:

                right_reserve = AndroidUtilities.dp(23)

            max_text_width = max(0, width - left_offset - right_reserve)

            title = self.textView

            if title is not None:

                title.measure(

                    jint(View.MeasureSpec.makeMeasureSpec(jint(max_text_width), View.MeasureSpec.AT_MOST)),

                    jint(View.MeasureSpec.makeMeasureSpec(jint(AndroidUtilities.dp(20)), View.MeasureSpec.EXACTLY))

                )

            sub.setMaxLines(jint(3))

            sub.measure(

                jint(View.MeasureSpec.makeMeasureSpec(jint(max_text_width), View.MeasureSpec.AT_MOST)),

                jint(View.MeasureSpec.makeMeasureSpec(jint(AndroidUtilities.dp(100)), View.MeasureSpec.AT_MOST))

            )

            title_height = title.getMeasuredHeight() if title is not None else AndroidUtilities.dp(20)

            sub_height = sub.getMeasuredHeight()

            total_height = AndroidUtilities.dp(10 + 10 + 4) + title_height + sub_height

            total_height = max(AndroidUtilities.dp(64), total_height)

            self.setMeasuredDimension(jint(width), jint(total_height))

        except Exception as e:

            try:

                from android_utils import log

                import traceback

                log(f"aLibary EnabledTextCell onMeasure error: {e}")

                log(traceback.format_exc())

            except Exception:

                pass

    @joverride()

    def onLayout(self, changed: bool, left: int, top: int, right: int, bottom: int):

        super().onLayout(changed, left, top, right, bottom)

        try:

            from org.telegram.messenger import AndroidUtilities, LocaleController

            from java import jint

            from android.view import Gravity

            height = bottom - top

            width = right - left

            title = self.textView

            value_tv = self.valueTextView

            img = self.imageView

            chk = self.getCheckBox()

            sub = _get_subtitle_view(self)

            sub_text = sub.getText() if sub is not None else None

            has_subtitle = sub is not None and sub.getVisibility() == 0 and sub_text is not None and str(sub_text).strip() != ""

            if has_subtitle:

                target_center = height // 2

            else:

                if title is not None and title.getVisibility() == 0:

                    target_center = title.getTop() + title.getMeasuredHeight() // 2

                else:

                    target_center = height // 2

            if img is not None and img.getVisibility() == 0:

                try:

                    from android.widget import ImageView

                    img.setScaleType(ImageView.ScaleType.CENTER)

                except Exception:

                    pass

                try:

                    img.setPadding(img.getPaddingLeft(), 0, img.getPaddingRight(), 0)

                except Exception:

                    pass

                img_h = img.getMeasuredHeight()

                img_top = target_center - img_h // 2

                img.layout(jint(img.getLeft()), jint(img_top), jint(img.getRight()), jint(img_top + img_h))

            if chk is not None and chk.getVisibility() == 0:

                chk_h = chk.getMeasuredHeight()

                chk_top = target_center - chk_h // 2

                chk.layout(jint(chk.getLeft()), jint(chk_top), jint(chk.getRight()), jint(chk_top + chk_h))

            if value_tv is not None and value_tv.getVisibility() == 0:

                try:

                    if title is not None:

                        value_tv.setTextSize(0, title.getTextSize())

                        value_tv.setTypeface(title.getTypeface())

                    value_tv.setGravity(Gravity.CENTER_VERTICAL | (Gravity.LEFT if LocaleController.isRTL else Gravity.RIGHT))

                    value_tv.setPadding(value_tv.getPaddingLeft(), 0, value_tv.getPaddingRight(), 0)

                except Exception:

                    pass

                val_h = value_tv.getMeasuredHeight()

                val_top = target_center - val_h // 2

                value_tv.layout(jint(value_tv.getLeft()), jint(val_top), jint(value_tv.getRight()), jint(val_top + val_h))

            if title is not None:

                try:

                    title.setGravity(Gravity.CENTER_VERTICAL | (Gravity.RIGHT if LocaleController.isRTL else Gravity.LEFT))

                    title.setPadding(title.getPaddingLeft(), 0, title.getPaddingRight(), 0)

                except Exception:

                    pass

            if has_subtitle:

                title_height = title.getMeasuredHeight()

                sub_height = sub.getMeasuredHeight()

                gap = AndroidUtilities.dp(4)

                total_text_height = title_height + gap + sub_height

                title_top = (height - total_text_height) // 2

                has_icon = img is not None and img.getVisibility() == 0

                text_left = AndroidUtilities.dp(self.offsetFromImage if has_icon else self.leftPadding)

                if LocaleController.isRTL:

                    t_left = width - title.getMeasuredWidth() - text_left

                else:

                    t_left = text_left

                title.layout(jint(t_left), jint(title_top), jint(t_left + title.getMeasuredWidth()), jint(title_top + title_height))

                sub_top = title_top + title_height + gap

                if LocaleController.isRTL:

                    s_left = width - sub.getMeasuredWidth() - text_left

                else:

                    s_left = text_left

                sub.layout(jint(s_left), jint(sub_top), jint(s_left + sub.getMeasuredWidth()), jint(sub_top + sub_height))

        except Exception as e:

            try:

                from android_utils import log

                import traceback

                log(f"aLibary EnabledTextCell onLayout error: {e}")

                log(traceback.format_exc())

            except Exception:

                pass

if has_android and has_slide_view:
    @java_subclass(SlideIntChooseView)
    class EnabledSlideView(Base):
        @joverride()
        def setEnabled(self, enabled):
            super().setEnabled(True)
else:
    class EnabledSlideView(Base):
        def setEnabled(self, enabled):
            pass

@java_subclass(FrameLayout)

class EnabledFrameLayout(Base):

    @joverride()

    def setEnabled(self, enabled):

        super().setEnabled(True)

def _run_safe(callback, val):

    try:

        from android.os import Looper

        if Looper.myLooper() == Looper.getMainLooper():

            callback(val)

            return

    except ImportError:

        pass

    try:

        from android_utils import run_on_ui_thread

        run_on_ui_thread(lambda: callback(val))

    except ImportError:

        callback(val)

def bind_state(view, state, callback):

    if not isinstance(state, State):

        return

    try:

        from android.view import View

        from java import dynamic_proxy

        import weakref

        class AttachListener(dynamic_proxy(View.OnAttachStateChangeListener)):

            def __init__(self, state_obj, cb):

                super().__init__()

                self.state_ref = weakref.ref(state_obj)

                self.cb = cb

                self.is_listening = False

            def onViewAttachedToWindow(self, v):

                if not self.is_listening:

                    state = self.state_ref()

                    if state:

                        state.add_listener(self.cb)

                        self.is_listening = True

            def onViewDetachedFromWindow(self, v):

                if self.is_listening:

                    state = self.state_ref()

                    if state:

                        state.remove_listener(self.cb)

                    self.is_listening = False

                try:

                    v.removeOnAttachStateChangeListener(self)

                except Exception:

                    pass

                try:

                    if hasattr(v, "_attach_listeners") and self in v._attach_listeners:

                        v._attach_listeners.remove(self)

                except Exception:

                    pass

        listener = AttachListener(state, callback)

        view.addOnAttachStateChangeListener(listener)

        if not hasattr(view, "_attach_listeners"):

            view._attach_listeners = []

        view._attach_listeners.append(listener)

        if hasattr(view, "isAttachedToWindow") and view.isAttachedToWindow():

            listener.onViewAttachedToWindow(view)

    except Exception:

        state.add_listener(callback)


def _jni_int(val):
    if val is None:
        return 0
    if val > 0x7FFFFFFF:
        return val - 0x100000000
    return val

class Widget:

    def __init__(self, width="wrap", height="wrap", weight=0.0, gravity=None, margins=None, padding=None):

        self.width = width

        self.height = height

        self.weight = weight

        self.gravity = gravity

        self.margins = margins

        self.padding = padding

    def build(self, context) -> Any:

        raise NotImplementedError()

    def generate_layout_params(self, parent_type: str, parent_view=None) -> Any:

        from org.telegram.messenger import AndroidUtilities

        w = -1 if self.width == "match" else (-2 if self.width == "wrap" else self.width)

        h = -1 if self.height == "match" else (-2 if self.height == "wrap" else self.height)

        if isinstance(w, int) and w > 0:

            w = AndroidUtilities.dp(w)

        if isinstance(h, int) and h > 0:

            h = AndroidUtilities.dp(h)

        if parent_type == "linear":

            from android.widget import LinearLayout

            if self.weight > 0.0:

                if parent_view is not None:

                    if parent_view.getOrientation() == LinearLayout.HORIZONTAL:

                        w = 0

                    else:

                        h = 0

                else:

                    w = 0

            lp = LinearLayout.LayoutParams(w, h)

            if self.weight > 0.0:

                lp.weight = float(self.weight)

            if self.gravity is not None:

                lp.gravity = self.gravity

        elif parent_type == "frame":

            from android.widget import FrameLayout

            from android.view import Gravity

            g = self.gravity if self.gravity is not None else (Gravity.TOP | Gravity.LEFT)

            lp = FrameLayout.LayoutParams(w, h, g)

        else:

            from android.view import ViewGroup

            lp = ViewGroup.LayoutParams(w, h)

        if self.margins is not None:

            if isinstance(self.margins, int):

                m = AndroidUtilities.dp(self.margins)

                lp.setMargins(m, m, m, m)

            elif isinstance(self.margins, (list, tuple)) and len(self.margins) == 4:

                l = AndroidUtilities.dp(self.margins[0])

                t = AndroidUtilities.dp(self.margins[1])

                r = AndroidUtilities.dp(self.margins[2])

                b = AndroidUtilities.dp(self.margins[3])

                lp.setMargins(l, t, r, b)

        return lp

    def apply_padding(self, view):

        if self.padding is not None:

            from org.telegram.messenger import AndroidUtilities

            if isinstance(self.padding, int):

                p = AndroidUtilities.dp(self.padding)

                view.setPadding(p, p, p, p)

            elif isinstance(self.padding, (list, tuple)) and len(self.padding) == 4:

                l = AndroidUtilities.dp(self.padding[0])

                t = AndroidUtilities.dp(self.padding[1])

                r = AndroidUtilities.dp(self.padding[2])

                b = AndroidUtilities.dp(self.padding[3])

                view.setPadding(l, t, r, b)

class Container(Widget):

    def __init__(self, children=None, **kwargs):

        if "width" not in kwargs:

            kwargs["width"] = "match"

        super().__init__(**kwargs)

        self.children = children or []

    def build_children(self, parent_view, parent_type: str, context):

        for child in self.children:

            if isinstance(child, Widget):

                child_view = child.build(context)

                lp = child.generate_layout_params(parent_type, parent_view)

                parent_view.addView(child_view, lp)

class VBox(Container):

    def build(self, context) -> Any:

        from android.widget import LinearLayout

        layout = LinearLayout(context)

        layout.setOrientation(LinearLayout.VERTICAL)

        self.apply_padding(layout)

        self.build_children(layout, "linear", context)

        return layout

class HBox(Container):

    def build(self, context) -> Any:

        from android.widget import LinearLayout

        layout = LinearLayout(context)

        layout.setOrientation(LinearLayout.HORIZONTAL)

        self.apply_padding(layout)

        self.build_children(layout, "linear", context)

        return layout

class Card(Container):

    def __init__(self, children=None, show_dividers=True, radius=20, **kwargs):

        if "width" not in kwargs:

            kwargs["width"] = "match"

        if "margins" not in kwargs:

            kwargs["margins"] = [12, 8, 12, 8]

        if "padding" not in kwargs:

            kwargs["padding"] = [0, 8, 0, 8]

        super().__init__(children=children, **kwargs)

        self.show_dividers = show_dividers

        self.radius = radius

    def build(self, context) -> Any:

        from android.widget import LinearLayout

        from android.view import View

        from org.telegram.ui.ActionBar import Theme

        from org.telegram.messenger import AndroidUtilities

        from android.graphics.drawable import GradientDrawable

        layout = LinearLayout(context)

        layout.setOrientation(LinearLayout.VERTICAL)

        self.apply_padding(layout)

        d = GradientDrawable()

        d.setShape(GradientDrawable.RECTANGLE)

        d.setCornerRadius(float(AndroidUtilities.dp(self.radius)))

        d.setColor(Theme.getColor(Theme.key_windowBackgroundWhite))

        layout.setBackground(d)

        layout.setClipToOutline(True)

        for idx, child in enumerate(self.children):

            if isinstance(child, Widget):

                if self.show_dividers and idx > 0:

                    divider = View(context)

                    divider.setBackgroundColor(Theme.getColor(Theme.key_divider))

                    from org.telegram.ui.Components import LayoutHelper

                    layout.addView(divider, LayoutHelper.createLinear(-1, 1, 0.0, 16, 0, 16, 0))

                child_view = child.build(context)

                lp = child.generate_layout_params("linear", layout)

                layout.addView(child_view, lp)

        return layout

class Label(Widget):

    def __init__(self, text, text_size=16, color=None, bold=False, **kwargs):

        super().__init__(**kwargs)

        self.text = text

        self.text_size = text_size

        self.color = color

        self.bold = bold

    def build(self, context) -> Any:

        from android.widget import TextView

        from android.util import TypedValue

        from android.graphics import Typeface

        view = TextView(context)

        self.apply_padding(view)

        view.setTextSize(TypedValue.COMPLEX_UNIT_DIP, self.text_size)

        if self.bold:

            view.setTypeface(None, Typeface.BOLD)

        if self.color is not None:

            view.setTextColor(_jni_int(self.color))

        else:

            from org.telegram.ui.ActionBar import Theme

            view.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))

        if isinstance(self.text, State):

            def update_text(v):

                view.setText(str(v))

                parent = view.getParent()

                if parent is not None:

                    parent.requestLayout()

            bind_state(view, self.text, update_text)

        else:

            view.setText(str(self.text))

        return view

class Field(Widget):

    def __init__(self, text="", hint="", on_change=None, **kwargs):

        super().__init__(**kwargs)

        self.text = text

        self.hint = hint

        self.on_change = on_change

    def build(self, context) -> Any:

        from android.widget import EditText

        from android.text import TextWatcher

        from java import dynamic_proxy

        view = EditText(context)

        from org.telegram.ui.ActionBar import Theme

        view.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))

        view.setHintTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteHintText))

        background = view.getBackground()

        if background is not None:

            from android.graphics import PorterDuff

            background.setColorFilter(Theme.getColor(Theme.key_windowBackgroundWhiteInputField), PorterDuff.Mode.SRC_IN)

        if self.hint:

            view.setHint(str(self.hint))

        if isinstance(self.text, State):

            self._updating_from_state = False

            bind_state(view, self.text, lambda v: self._set_text_safe(view, v))

        else:

            view.setText(str(self.text))

        class Watcher(dynamic_proxy(TextWatcher)):

            def __init__(self, outer):

                super().__init__()

                self.outer = outer

            def beforeTextChanged(self, s, start, count, after): pass

            def onTextChanged(self, s, start, before, count):

                val = str(s)

                if isinstance(self.outer.text, State):

                    self.outer._updating_from_state = True

                    self.outer.text.set(val)

                    self.outer._updating_from_state = False

                if self.outer.on_change:

                    self.outer.on_change(val)

            def afterTextChanged(self, s): pass

        view.addTextChangedListener(Watcher(self))

        self.apply_padding(view)

        from org.telegram.messenger import AndroidUtilities

        left_pad = AndroidUtilities.dp(self.padding[0]) if (isinstance(self.padding, (list, tuple)) and len(self.padding) == 4) else (AndroidUtilities.dp(self.padding) if isinstance(self.padding, int) else 0)

        view.setPadding(left_pad, view.getPaddingTop(), view.getPaddingRight(), view.getPaddingBottom())

        return view

    def _set_text_safe(self, view, val):

        if not getattr(self, "_updating_from_state", False):

            current = str(view.getText())

            new_val_str = str(val)

            if current != new_val_str:

                cursor_pos = view.getSelectionStart()

                view.setText(new_val_str)

                if view.isFocused() and cursor_pos >= 0:

                    view.setSelection(min(cursor_pos, len(new_val_str)))

class Button(Widget):

    def __init__(self, text, on_click=None, text_gravity=None, **kwargs):

        if "width" not in kwargs:

            kwargs["width"] = "match"

        super().__init__(**kwargs)

        self.text = text

        self.on_click = on_click

        self.text_gravity = text_gravity

    def build(self, context) -> Any:

        from android.widget import TextView

        from android.view import Gravity

        from android_utils import OnClickListener

        view = TextView(context)

        self.apply_padding(view)

        g = self.text_gravity if self.text_gravity is not None else (Gravity.LEFT | Gravity.CENTER_VERTICAL)

        view.setGravity(g)

        from org.telegram.ui.ActionBar import Theme

        view.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlueText2))

        if isinstance(self.text, State):

            bind_state(view, self.text, lambda v: view.setText(str(v)))

        else:

            view.setText(str(self.text))

        if self.on_click:

            view.setOnClickListener(OnClickListener(self.on_click))

        return view

class Icon(Widget):

    def __init__(self, name, size=24, color=None, **kwargs):

        if "width" not in kwargs:

            kwargs["width"] = size

        if "height" not in kwargs:

            kwargs["height"] = size

        super().__init__(**kwargs)

        self.name = name

        self.size = size

        self.color = color

    def build(self, context) -> Any:

        from org.telegram.ui.Components import BackupImageView

        from org.telegram.messenger import AndroidUtilities

        view = BackupImageView(context)

        sz = AndroidUtilities.dp(self.size)

        try:

            ctx = context.getApplicationContext()

            res_id = ctx.getResources().getIdentifier(self.name, "drawable", ctx.getPackageName())

            if res_id != 0:

                view.setImageResource(res_id)

        except Exception:

            pass

        if self.color is not None:

            from android.graphics import PorterDuff, PorterDuffColorFilter

            view.setColorFilter(PorterDuffColorFilter(_jni_int(self.color), PorterDuff.Mode.SRC_IN))

        return view

class Toggle(Widget):

    def __init__(self, value, on_change=None, **kwargs):

        super().__init__(**kwargs)

        self.value = value

        self.on_change = on_change

    def build(self, context) -> Any:

        try:

            from org.telegram.ui.Components import Switch as TelegramSwitch

            from org.telegram.ui.ActionBar import Theme

            view = TelegramSwitch(context)

            view.setColors(Theme.key_switchTrack, Theme.key_switchTrackChecked, Theme.key_windowBackgroundWhite, Theme.key_windowBackgroundWhite)

        except ImportError:

            class MockSwitch:

                def __init__(self, ctx):

                    self._checked = False

                    self._listener = None

                def setColors(self, a, b, c, d): pass

                def setChecked(self, checked, animated):

                    self._checked = checked

                    if self._listener:

                        self._listener.onCheckedChanged(self, checked)

                def isChecked(self): return self._checked

                def setOnCheckedChangeListener(self, listener): self._listener = listener

            view = MockSwitch(context)

        if isinstance(self.value, State):

            self._updating_from_state = False

            bind_state(view, self.value, lambda v: self._set_checked_safe(view, v))

        else:

            view.setChecked(bool(self.value), False)

        from java import dynamic_proxy

        try:

            from org.telegram.ui.Components import Switch as TelegramSwitch

            OnCheckedChangeListener = getattr(TelegramSwitch, "OnCheckedChangeListener")

        except Exception:

            class OnCheckedChangeListener: pass

        class ToggleListener(dynamic_proxy(OnCheckedChangeListener)):

            def __init__(self, outer):

                super().__init__()

                self.outer = outer

            def onCheckedChanged(self, buttonView, isChecked):

                if isinstance(self.outer.value, State):

                    self.outer._updating_from_state = True

                    self.outer.value.set(isChecked)

                    self.outer._updating_from_state = False

                if self.outer.on_change:

                    self.outer.on_change(isChecked)

        view.setOnCheckedChangeListener(ToggleListener(self))

        return view

    def _set_checked_safe(self, view, val):

        if not getattr(self, "_updating_from_state", False):

            view.setChecked(bool(val), True)

class Radio(Widget):

    def __init__(self, value, checked_value, on_change=None, **kwargs):

        if "width" not in kwargs:

            kwargs["width"] = 18

        if "height" not in kwargs:

            kwargs["height"] = 18

        super().__init__(**kwargs)

        self.value = value

        self.checked_value = checked_value

        self.on_change = on_change

    def build(self, context) -> Any:

        try:

            from android.widget import FrameLayout

            from android.view import View, Gravity

            from org.telegram.messenger import AndroidUtilities

            from org.telegram.ui.ActionBar import Theme

            from android.graphics.drawable import GradientDrawable

            from org.telegram.ui.Components import LayoutHelper

        except ImportError:

            class MockView:

                def setBackground(self, bg): pass

                def setVisibility(self, vis): pass

                def setClickable(self, click): pass

            class MockFrameLayout(MockView):

                def addView(self, child, lp=None): pass

            return MockFrameLayout()

        def _alpha(color, opacity):

            return (color & 0x00FFFFFF) | (int(opacity * 255) << 24)

        try:

            accent = Theme.getColor(Theme.key_radioBackgroundChecked)

            if accent == 0 or accent is None:

                accent = Theme.getColor(Theme.key_featuredStickers_addButton)

            inactive_color = Theme.getColor(Theme.key_radioBackground)

            if inactive_color == 0 or inactive_color is None:

                inactive_color = _alpha(Theme.getColor(Theme.key_dialogTextBlack), 0.25)

        except Exception:

            accent = 0xFF3390EC

            inactive_color = 0x3F000000

        def _circle_outline(color):

            d = GradientDrawable()

            d.setShape(GradientDrawable.OVAL)

            d.setStroke(AndroidUtilities.dp(2), _jni_int(color))

            d.setColor(0)

            return d

        def _circle_solid(color):

            d = GradientDrawable()

            d.setShape(GradientDrawable.OVAL)

            d.setColor(_jni_int(color))

            return d

        radio_frame = FrameLayout(context)

        radio_frame.setClickable(False)

        radio_frame.setFocusable(False)

        val = self.value.get() if isinstance(self.value, State) else self.value

        active = val == self.checked_value

        outer = View(context)

        outer.setBackground(_circle_outline(accent if active else inactive_color))

        radio_frame.addView(outer, LayoutHelper.createFrame(16, 16, Gravity.CENTER))

        inner = View(context)

        inner.setBackground(_circle_solid(accent))

        inner.setVisibility(0 if active else 4)

        radio_frame.addView(inner, LayoutHelper.createFrame(8, 8, Gravity.CENTER))

        if isinstance(self.value, State):

            def on_state_changed(new_val):

                is_active = new_val == self.checked_value

                outer.setBackground(_circle_outline(accent if is_active else inactive_color))

                inner.setVisibility(0 if is_active else 4)

            bind_state(radio_frame, self.value, on_state_changed)

            radio_frame._state_listener = on_state_changed

        return radio_frame

class RowItem(Widget):

    def __init__(self, title, subtext=None, icon=None, right_widget=None, on_click=None, height=None, **kwargs):

        if "width" not in kwargs:

            kwargs["width"] = "match"

        super().__init__(**kwargs)

        self.title = title

        self.subtext = subtext

        self.icon = icon

        self.right_widget = right_widget

        self.on_click = on_click

        self.row_height = height

    def build(self, context) -> Any:

        from org.telegram.ui.Cells import TextCell

        from android_utils import OnClickListener

        is_native_toggle = False

        is_native_label = False

        if self.right_widget is not None:

            if self.right_widget.__class__.__name__ == 'Toggle':

                is_native_toggle = True

            elif self.right_widget.__class__.__name__ == 'Label':

                is_native_label = False

        if self.right_widget is not None and not is_native_toggle and not is_native_label:

            return self._build_custom_fallback(context)

        res_id = 0

        if self.icon:

            try:

                ctx = context.getApplicationContext()

                res_id = ctx.getResources().getIdentifier(str(self.icon), "drawable", ctx.getPackageName())

            except Exception:

                pass

        from java import jint

        if is_native_toggle:

            cell = EnabledTextCell.new_java_instance(context, jint(23), False, True, None)

            if res_id != 0:

                cell.leftPadding = 75

            else:

                cell.leftPadding = 23

        else:

            cell = EnabledTextCell.new_java_instance(context, jint(23), False, False, None)

        title_str = str(self.title.get()) if isinstance(self.title, State) else str(self.title)

        if is_native_toggle:

            toggle = self.right_widget

            val = toggle.value

            checked = val.get() if isinstance(val, State) else bool(val)

            if res_id != 0:

                cell.setTextAndCheckAndIcon(title_str, checked, res_id, False)

            else:

                cell.setTextAndCheck(title_str, checked, False)

            if isinstance(val, State):

                def on_state_changed(v):

                    cell.setChecked(bool(v))

                bind_state(cell, val, on_state_changed)

                cell._state_listener = on_state_changed

            def on_cell_click(view):

                current_val = val.get() if isinstance(val, State) else bool(val)

                new_val = not current_val

                if isinstance(val, State):

                    val.set(new_val)

                if toggle.on_change:

                    toggle.on_change(new_val)

                if self.on_click:

                    self.on_click(view)

            cell.setOnClickListener(OnClickListener(on_cell_click))

        elif is_native_label:

            lbl = self.right_widget

            lbl_val = lbl.text

            lbl_str = str(lbl_val.get()) if isinstance(lbl_val, State) else str(lbl_val)

            if res_id != 0:

                cell.setTextAndValueAndIcon(title_str, lbl_str, res_id, False)

            else:

                cell.setTextAndValue(title_str, lbl_str, False)

            if isinstance(lbl_val, State):

                def on_label_changed(v):

                    try:

                        cell.valueTextView.setText(str(v), True)

                        cell.requestLayout()

                    except Exception:

                        pass

                bind_state(cell, lbl_val, on_label_changed)

                cell._label_listener = on_label_changed

            if self.on_click:

                cell.setOnClickListener(OnClickListener(self.on_click))

        else:

            if res_id != 0:

                cell.setTextAndIcon(title_str, res_id, False)

            else:

                cell.setText(title_str, False)

            if self.on_click:

                cell.setOnClickListener(OnClickListener(self.on_click))

        if self.row_height is not None:

            cell.heightDp = self.row_height

        elif self.subtext:

            subtext_str = str(self.subtext.get()) if isinstance(self.subtext, State) else str(self.subtext)

            cell.setSubtitle(subtext_str)

            cell.heightDp = 64

            if isinstance(self.subtext, State):

                def on_subtext_changed(v):

                    try:

                        cell.setSubtitle(str(v))

                        cell.requestLayout()

                    except Exception:

                        pass

                bind_state(cell, self.subtext, on_subtext_changed)

        if isinstance(self.title, State):

            def on_title_changed(v):

                try:

                    cell.textView.setText(str(v))

                    cell.requestLayout()

                except Exception:

                    pass

            bind_state(cell, self.title, on_title_changed)

        return cell

    def _build_custom_fallback(self, context) -> Any:

        from android.view import Gravity

        from android.widget import FrameLayout, LinearLayout, TextView

        from android.util import TypedValue

        from android.text import TextUtils

        from org.telegram.messenger import AndroidUtilities, LocaleController

        from org.telegram.ui.ActionBar import Theme

        from org.telegram.ui.Components import LayoutHelper

        from android_utils import OnClickListener

        container = EnabledFrameLayout.new_java_instance(context)

        container.setBackground(Theme.getSelectorDrawable(True))

        if self.on_click:

            container.setOnClickListener(OnClickListener(self.on_click))

        left_offset = 23

        if self.icon:

            left_offset = 71

            res_id = 0

            try:

                ctx = context.getApplicationContext()

                res_id = ctx.getResources().getIdentifier(str(self.icon), "drawable", ctx.getPackageName())

            except Exception:

                pass

            if res_id != 0:

                icon_widget = Icon(self.icon, size=24, color=Theme.getColor(Theme.key_windowBackgroundWhiteGrayIcon))

                icon_view = icon_widget.build(context)

                container.addView(icon_view, LayoutHelper.createFrame(24, 24, (Gravity.RIGHT if LocaleController.isRTL else Gravity.LEFT) | Gravity.CENTER_VERTICAL, 21, 0, 21, 0))

        text_container = LinearLayout(context)

        text_container.setOrientation(LinearLayout.VERTICAL)

        title_view = TextView(context)

        title_view.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))

        title_view.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16)

        title_view.setLines(1)

        title_view.setMaxLines(1)

        title_view.setSingleLine(True)

        title_view.setEllipsize(TextUtils.TruncateAt.END)

        title_view.setGravity(Gravity.RIGHT if LocaleController.isRTL else Gravity.LEFT)

        title_view.setIncludeFontPadding(False)

        title_str = str(self.title.get()) if isinstance(self.title, State) else str(self.title)

        title_view.setText(title_str)

        if isinstance(self.title, State):

            def on_title_changed(v):

                title_view.setText(str(v))

            bind_state(container, self.title, on_title_changed)

            container._title_listener = on_title_changed

        text_gravity = (Gravity.RIGHT if LocaleController.isRTL else Gravity.LEFT)

        text_container.addView(title_view, LayoutHelper.createLinear(-1, -2, text_gravity))

        if self.subtext:

            sub_view = TextView(context)

            sub_view.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText2))

            sub_view.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)

            sub_view.setSingleLine(False)

            sub_view.setMaxLines(2)

            sub_view.setEllipsize(TextUtils.TruncateAt.END)

            sub_view.setGravity(Gravity.RIGHT if LocaleController.isRTL else Gravity.LEFT)

            sub_view.setIncludeFontPadding(False)

            sub_str = str(self.subtext.get()) if isinstance(self.subtext, State) else str(self.subtext)

            sub_view.setText(sub_str)

            if isinstance(self.subtext, State):

                def on_subtext_changed(v):

                    sub_view.setText(str(v))

                bind_state(container, self.subtext, on_subtext_changed)

                container._sub_listener = on_subtext_changed

            text_container.addView(sub_view, LayoutHelper.createLinear(-1, -2, text_gravity, 0, 4, 0, 0))

        content_layout = LinearLayout(context)

        content_layout.setOrientation(LinearLayout.HORIZONTAL)

        content_left = left_offset if not LocaleController.isRTL else 22

        content_right = 22 if not LocaleController.isRTL else left_offset

        container.addView(content_layout, LayoutHelper.createFrame(-1, -2, Gravity.CENTER_VERTICAL, content_left, 0, content_right, 0))

        lp_text = LayoutHelper.createLinear(0, -2)

        lp_text.weight = float(1.0)

        content_layout.addView(text_container, lp_text)

        if self.right_widget is not None:

            right_view = self.right_widget.build(context)

            if self.right_widget.__class__.__name__ == 'Toggle':

                toggle = self.right_widget

                val = toggle.value

                def on_cell_click(view):

                    current_val = val.get() if isinstance(val, State) else bool(val)

                    new_val = not current_val

                    if isinstance(val, State):

                        val.set(new_val)

                    if toggle.on_change:

                        toggle.on_change(new_val)

                    if self.on_click:

                        self.on_click(view)

                container.setOnClickListener(OnClickListener(on_cell_click))

                w, h = 37, 20

            elif self.right_widget.__class__.__name__ == 'Radio':

                radio = self.right_widget

                val = radio.value

                def on_cell_click(view):

                    if isinstance(val, State):

                        val.set(radio.checked_value)

                    if radio.on_change:

                        radio.on_change(radio.checked_value)

                    if self.on_click:

                        self.on_click(view)

                container.setOnClickListener(OnClickListener(on_cell_click))

                w, h = 18, 18

            elif self.right_widget.__class__.__name__ == 'Label':

                lbl = self.right_widget

                lbl_val = lbl.text

                if isinstance(lbl_val, State):

                    def on_label_changed(v):

                        right_view.setText(str(v))

                    bind_state(container, lbl_val, on_label_changed)

                    container._label_listener = on_label_changed

                w, h = -2, -2

            else:

                w, h = -2, -2

            gap_left = 12 if not LocaleController.isRTL else 0

            gap_right = 0 if not LocaleController.isRTL else 12

            content_layout.addView(right_view, LayoutHelper.createLinear(w, h, Gravity.CENTER_VERTICAL, gap_left, 0, gap_right, 0))

        cell_height = self.row_height if self.row_height is not None else (72 if self.subtext else 50)

        container.setMinimumHeight(AndroidUtilities.dp(cell_height))

        lp = FrameLayout.LayoutParams(FrameLayout.LayoutParams.MATCH_PARENT, AndroidUtilities.dp(cell_height))

        container.setLayoutParams(lp)

        return container

class Selector(Widget):

    def __init__(self, text, items, value, on_change=None, icon=None, **kwargs):

        if "width" not in kwargs:

            kwargs["width"] = "match"

        super().__init__(**kwargs)

        self.text = text

        self.items = items

        self.value = value

        self.on_change = on_change

        self.icon = icon

    def build(self, context) -> Any:

        from org.telegram.ui.ActionBar import Theme

        current_text_state = State("")

        def update_label(val):

            try:

                idx = int(val)

                if 0 <= idx < len(self.items):

                    current_text_state.set(self.items[idx])

            except Exception:

                pass

        if not isinstance(self.value, State):

            update_label(self.value)

        right_lbl = Label(text=current_text_state, text_size=15, color=Theme.getColor(Theme.key_windowBackgroundWhiteBlueText2))

        def open_dialog(view):

            from ui.alert import AlertDialogBuilder

            builder = AlertDialogBuilder(context)

            builder.set_title(str(self.text))

            def on_select(bld, index):

                if isinstance(self.value, State):

                    self.value.set(index)

                if self.on_change:

                    self.on_change(index)

                bld.dismiss()

            builder.set_items(self.items, on_select)

            builder.show()

        row = RowItem(

            title=self.text,

            icon=self.icon,

            right_widget=right_lbl,

            on_click=open_dialog

        )

        cell = row.build(context)

        if isinstance(self.value, State):

            bind_state(cell, self.value, update_label)

        return cell

def to_setting(widget: Widget) -> Any:

    from ui.settings import Custom, SimpleSettingFactory

    def create_view(context, list_view, current_account, class_guid, resources_provider):

        try:

            from android_utils import log

            from android.view import ViewGroup

            log("aLibary to_setting: building widget")

            if hasattr(widget, "build_with_provider"):

                view = widget.build_with_provider(context, resources_provider)

            else:

                view = widget.build(context)

            log("aLibary to_setting: widget built successfully")

            lp = ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)

            view.setLayoutParams(lp)

            view.setClickable(True)

            return view

        except Exception as e:

            from android_utils import log

            import traceback

            log(f"aLibary to_setting error: {e}")

            log(traceback.format_exc())

            try:

                from android.view import View

                blank_view = View(context)

                from android.view import ViewGroup

                lp = ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0)

                blank_view.setLayoutParams(lp)

                return blank_view

            except Exception:

                return None

    factory = SimpleSettingFactory(

        create_view,

        bind_view=lambda *args: None,

        is_clickable=False,

        is_shadow=False

    )

    return Custom(factory=factory.instance.java)

class Slider(Widget):

    def __init__(self, value, min_val, max_val, on_change=None, to_string=None, **kwargs):

        if "width" not in kwargs:

            kwargs["width"] = "match"

        super().__init__(**kwargs)

        self.value = value

        self.min_val = min_val

        self.max_val = max_val

        self.on_change = on_change

        self.to_string = to_string

    def build(self, context) -> Any:
        if has_android and has_slide_view:
            try:
                from org.telegram.ui.Cells import SlideIntChooseView
                from org.telegram.messenger import Utilities
                from java import dynamic_proxy

                view = EnabledSlideView.new_java_instance(context, None)

                class DummyCallback(dynamic_proxy(Utilities.CallbackReturn)):
                    def run(self, val):
                        return str(val)

                options = SlideIntChooseView.Options.make(
                    0,
                    self.min_val,
                    self.max_val,
                    DummyCallback()
                )

                class ToString2Callback(dynamic_proxy(Utilities.Callback2Return)):
                    def __init__(self, to_string):
                        super().__init__()
                        self.to_string = to_string

                    def run(self, label_type, val):
                        if self.to_string:
                            try:
                                res = self.to_string(int(label_type), int(val))
                                if res is not None:
                                    return str(res)
                            except Exception:
                                pass
                        return str(val)

                try:
                    field = options.getClass().getDeclaredField("toString")
                    field.setAccessible(True)
                    field.set(options, ToString2Callback(self.to_string))
                except Exception as e:
                    from android_utils import log
                    log(f"aLibary: failed to set toString field: {e}")
                    options.toString = ToString2Callback(self.to_string)

                class SeekBarCallback(dynamic_proxy(Utilities.Callback)):
                    def __init__(self, outer):
                        super().__init__()
                        self.outer = outer

                    def run(self, val_obj):
                        val = int(val_obj)
                        if isinstance(self.outer.value, State):
                            self.outer.value.set(val)
                        if self.outer.on_change:
                            self.outer.on_change(val)

                initial_val = self.value.get() if isinstance(self.value, State) else int(self.value)
                view.set(initial_val, options, SeekBarCallback(self))

                if isinstance(self.value, State):
                    def on_state_changed(v):
                        try:
                            progress = view.getProgress(int(v))
                            view.seekBarView.setProgress(progress, True)
                            view.updateTexts(int(v), True)
                        except Exception:
                            pass
                    bind_state(view, self.value, on_state_changed)

                view.setClickable(True)
                view.setFocusable(False)
                return view
            except Exception as e:
                from android_utils import log
                log(f"aLibary: SlideIntChooseView build failed: {e}. Falling back to standard SeekBar.")

        # Fallback to standard Android SeekBar Layout
        from android.widget import LinearLayout, SeekBar, TextView
        from android.view import ViewGroup
        from org.telegram.messenger import AndroidUtilities
        from org.telegram.ui.ActionBar import Theme
        from org.telegram.ui.Components import LayoutHelper
        from android.util import TypedValue
        from java import dynamic_proxy
        from hook_utils import find_class

        layout = LinearLayout(context)
        layout.setOrientation(LinearLayout.VERTICAL)
        layout.setPadding(AndroidUtilities.dp(21), AndroidUtilities.dp(8), AndroidUtilities.dp(21), AndroidUtilities.dp(8))
        layout.setMinimumHeight(AndroidUtilities.dp(64))

        value_text = TextView(context)
        value_text.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
        value_text.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16)
        
        initial_val = self.value.get() if isinstance(self.value, State) else int(self.value)
        
        def format_value(v):
            if self.to_string:
                try:
                    try:
                        res = self.to_string(0, int(v))
                    except TypeError:
                        try:
                            res = self.to_string(int(v))
                        except Exception:
                            res = str(v)
                    if res is not None:
                        return str(res)
                except Exception:
                    pass
            return str(v)

        value_text.setText(format_value(initial_val))
        layout.addView(value_text, LayoutHelper.createLinear(-1, -2))

        seek_bar = SeekBar(context)
        seek_bar.setMax(int(self.max_val) - int(self.min_val))
        seek_bar.setProgress(int(initial_val) - int(self.min_val))

        OnSeekBarChangeListener = find_class("android.widget.SeekBar$OnSeekBarChangeListener")
        
        class SeekBarChangeListener(dynamic_proxy(OnSeekBarChangeListener)):
            def __init__(self, outer, value_text_view):
                super().__init__()
                self.outer = outer
                self.value_text_view = value_text_view

            def onProgressChanged(self, seekbar, progress, from_user):
                val = progress + int(self.outer.min_val)
                self.value_text_view.setText(format_value(val))
                if from_user:
                    if isinstance(self.outer.value, State):
                        self.outer.value.set(val)
                    if self.outer.on_change:
                        self.outer.on_change(val)

            def onStartTrackingTouch(self, seekbar):
                pass

            def onStopTrackingTouch(self, seekbar):
                pass

        seek_bar.setOnSeekBarChangeListener(SeekBarChangeListener(self, value_text))
        layout.addView(seek_bar, LayoutHelper.createLinear(-1, -2, 0.0, 0, 4, 0, 0))

        if isinstance(self.value, State):
            def on_state_changed(v):
                try:
                    val = int(v)
                    seek_bar.setProgress(val - int(self.min_val))
                    value_text.setText(format_value(val))
                except Exception:
                    pass
            bind_state(layout, self.value, on_state_changed)

        layout.setClickable(True)
        layout.setFocusable(False)
        return layout

class AltSeekbar(Widget):

    def __init__(self, value, min_val, max_val, title, left_text, right_text, on_change=None, **kwargs):

        if "width" not in kwargs:

            kwargs["width"] = "match"

        super().__init__(**kwargs)

        self.value = value

        self.min_val = min_val

        self.max_val = max_val

        self.title = title

        self.left_text = left_text

        self.right_text = right_text

        self.on_change = on_change

    def build(self, context) -> Any:
        if has_android:
            try:
                from hook_utils import find_class
                from java import dynamic_proxy

                AltSeekbar_cls = find_class("com.exteragram.messenger.preferences.components.AltSeekbar")
                AltSeekbar_OnDrag = find_class("com.exteragram.messenger.preferences.components.AltSeekbar$OnDrag")

                if AltSeekbar_cls is not None and AltSeekbar_OnDrag is not None:
                    class SeekbarCallback(dynamic_proxy(AltSeekbar_OnDrag)):
                        def __init__(self, outer):
                            super().__init__()
                            self.outer = outer

                        def run(self, val):
                            if isinstance(self.outer.value, State):
                                self.outer.value.set(val)
                            if self.outer.on_change:
                                self.outer.on_change(val)

                    initial_val = self.value.get() if isinstance(self.value, State) else float(self.value)
                    view = AltSeekbar_cls(
                        context,
                        SeekbarCallback(self),
                        int(self.min_val),
                        int(self.max_val),
                        str(self.title),
                        str(self.left_text),
                        str(self.right_text)
                    )
                    view.setProgress(float(initial_val))

                    if isinstance(self.value, State):
                        def on_state_changed(v):
                            try:
                                view.setProgress(float(v))
                            except Exception:
                                pass
                        bind_state(view, self.value, on_state_changed)

                    view.setClickable(True)
                    view.setFocusable(False)
                    return view
            except Exception as e:
                from android_utils import log
                log(f"aLibary: custom AltSeekbar failed to build: {e}. Falling back to standard SeekBar.")

        # Fallback to standard SeekBar + Title + Left/Right text layout
        from android.widget import LinearLayout, SeekBar, TextView
        from android.view import ViewGroup, Gravity
        from org.telegram.messenger import AndroidUtilities
        from org.telegram.ui.ActionBar import Theme
        from org.telegram.ui.Components import LayoutHelper
        from android.util import TypedValue
        from java import dynamic_proxy
        from hook_utils import find_class

        layout = LinearLayout(context)
        layout.setOrientation(LinearLayout.VERTICAL)
        layout.setPadding(AndroidUtilities.dp(21), AndroidUtilities.dp(8), AndroidUtilities.dp(21), AndroidUtilities.dp(8))
        layout.setMinimumHeight(AndroidUtilities.dp(80))

        initial_val = self.value.get() if isinstance(self.value, State) else float(self.value)
        initial_val = int(round(initial_val))

        title_text = TextView(context)
        title_text.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
        title_text.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16)
        
        def get_title_str(v):
            return f"{self.title} ({v})"

        title_text.setText(get_title_str(initial_val))
        layout.addView(title_text, LayoutHelper.createLinear(-1, -2))

        seek_bar = SeekBar(context)
        seek_bar.setMax(int(self.max_val) - int(self.min_val))
        seek_bar.setProgress(initial_val - int(self.min_val))

        OnSeekBarChangeListener = find_class("android.widget.SeekBar$OnSeekBarChangeListener")
        
        class SeekBarChangeListener(dynamic_proxy(OnSeekBarChangeListener)):
            def __init__(self, outer, title_text_view):
                super().__init__()
                self.outer = outer
                self.title_text_view = title_text_view

            def onProgressChanged(self, seekbar, progress, from_user):
                val = progress + int(self.outer.min_val)
                self.title_text_view.setText(get_title_str(val))
                if from_user:
                    if isinstance(self.outer.value, State):
                        self.outer.value.set(val)
                    if self.outer.on_change:
                        self.outer.on_change(val)

            def onStartTrackingTouch(self, seekbar):
                pass

            def onStopTrackingTouch(self, seekbar):
                pass

        seek_bar.setOnSeekBarChangeListener(SeekBarChangeListener(self, title_text))
        layout.addView(seek_bar, LayoutHelper.createLinear(-1, -2, 0.0, 0, 4, 0, 0))

        labels_layout = LinearLayout(context)
        labels_layout.setOrientation(LinearLayout.HORIZONTAL)
        
        left_lbl = TextView(context)
        left_lbl.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
        left_lbl.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
        left_lbl.setText(str(self.left_text))

        right_lbl = TextView(context)
        right_lbl.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
        right_lbl.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
        right_lbl.setText(str(self.right_text))
        
        labels_layout.addView(left_lbl, LayoutHelper.createLinear(0, -2, 1.0))
        labels_layout.addView(right_lbl, LayoutHelper.createLinear(-2, -2))

        layout.addView(labels_layout, LayoutHelper.createLinear(-1, -2, 0.0, 0, 2, 0, 0))

        if isinstance(self.value, State):
            def on_state_changed(v):
                try:
                    val = int(round(float(v)))
                    seek_bar.setProgress(val - int(self.min_val))
                    title_text.setText(get_title_str(val))
                except Exception:
                    pass
            bind_state(layout, self.value, on_state_changed)

        layout.setClickable(True)
        layout.setFocusable(False)
        return layout

class ActionRow(Widget):

    def __init__(self, title, subtext=None, button_text="Add", on_button_click=None, on_click=None, icon=None, **kwargs):

        if "width" not in kwargs:

            kwargs["width"] = "match"

        super().__init__(**kwargs)

        self.title = title

        self.subtext = subtext

        self.button_text = button_text

        self.on_button_click = on_button_click

        self.on_click = on_click

        self.icon = icon

    def build(self, context) -> Any:

        from android.widget import FrameLayout, TextView

        from android.view import Gravity, ViewGroup

        from android.util import TypedValue

        from android.text import TextUtils

        from org.telegram.messenger import AndroidUtilities, LocaleController

        from org.telegram.ui.ActionBar import Theme

        from org.telegram.ui.Components import LayoutHelper, ProgressButton

        from android_utils import OnClickListener

        container = EnabledFrameLayout.new_java_instance(context)

        if self.on_click:

            container.setBackground(Theme.getSelectorDrawable(True))

            container.setOnClickListener(OnClickListener(self.on_click))

        else:

            container.setClickable(True)

            container.setFocusable(False)

        left_offset = 22

        if self.icon:

            left_offset = 71

            res_id = 0

            try:

                ctx = context.getApplicationContext()

                res_id = ctx.getResources().getIdentifier(str(self.icon), "drawable", ctx.getPackageName())

            except Exception:

                pass

            if res_id != 0:

                icon_widget = Icon(self.icon, size=24, color=Theme.getColor(Theme.key_windowBackgroundWhiteGrayIcon))

                icon_view = icon_widget.build(context)

                container.addView(icon_view, LayoutHelper.createFrame(24, 24, (Gravity.RIGHT if LocaleController.isRTL else Gravity.LEFT) | Gravity.CENTER_VERTICAL, 21, 0, 21, 0))

        from android.widget import LinearLayout

        text_container = LinearLayout(context)

        text_container.setOrientation(LinearLayout.VERTICAL)

        title_view = TextView(context)

        title_view.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))

        title_view.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16)

        title_view.setLines(1)

        title_view.setMaxLines(1)

        title_view.setSingleLine(True)

        title_view.setEllipsize(TextUtils.TruncateAt.END)

        title_view.setGravity(Gravity.RIGHT if LocaleController.isRTL else Gravity.LEFT)

        title_view.setIncludeFontPadding(False)

        title_str = str(self.title.get()) if isinstance(self.title, State) else str(self.title)

        title_view.setText(title_str)

        if isinstance(self.title, State):

            def on_title_changed(v):

                try:

                    title_view.setText(str(v))

                    container.requestLayout()

                except Exception:

                    pass

            bind_state(container, self.title, on_title_changed)

            container._title_listener = on_title_changed

        text_gravity = (Gravity.RIGHT if LocaleController.isRTL else Gravity.LEFT)

        text_container.addView(title_view, LayoutHelper.createLinear(-1, -2, text_gravity))

        if self.subtext:

            sub_view = TextView(context)

            sub_view.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText2))

            sub_view.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)

            sub_view.setSingleLine(False)

            sub_view.setMaxLines(3)

            sub_view.setEllipsize(TextUtils.TruncateAt.END)

            sub_view.setGravity(Gravity.RIGHT if LocaleController.isRTL else Gravity.LEFT)

            sub_view.setIncludeFontPadding(False)

            sub_str = str(self.subtext.get()) if isinstance(self.subtext, State) else str(self.subtext)

            sub_view.setText(sub_str)

            if isinstance(self.subtext, State):

                def on_sub_changed(v):

                    try:

                        sub_view.setText(str(v))

                        container.requestLayout()

                    except Exception:

                        pass

                bind_state(container, self.subtext, on_sub_changed)

            text_container.addView(sub_view, LayoutHelper.createLinear(-1, -2, text_gravity, 0, 2, 0, 0))

        text_left_margin = left_offset if not LocaleController.isRTL else 112

        text_right_margin = 112 if not LocaleController.isRTL else left_offset

        container.addView(text_container, LayoutHelper.createFrame(-1, -2, text_gravity | Gravity.CENTER_VERTICAL, text_left_margin, 0, text_right_margin, 0))

        btn = ProgressButton(context)

        btn_str = str(self.button_text.get()) if isinstance(self.button_text, State) else str(self.button_text)

        btn.setText(btn_str)

        if isinstance(self.button_text, State):

            def on_btn_text_changed(v):

                btn.setText(str(v))

            bind_state(container, self.button_text, on_btn_text_changed)

        btn.setTextColor(Theme.getColor(Theme.key_featuredStickers_buttonText))

        btn.setProgressColor(Theme.getColor(Theme.key_featuredStickers_buttonProgress))

        btn.setBackgroundRoundRect(Theme.getColor(Theme.key_featuredStickers_addButton), Theme.getColor(Theme.key_featuredStickers_addButtonPressed))

        if self.on_button_click:

            btn.setOnClickListener(OnClickListener(self.on_button_click))

        container.addView(btn, LayoutHelper.createFrame(-2, 28, (Gravity.LEFT if LocaleController.isRTL else Gravity.RIGHT) | Gravity.CENTER_VERTICAL, 19, 0, 19, 0))

        container.setPadding(0, AndroidUtilities.dp(12), 0, AndroidUtilities.dp(12))

        container.setMinimumHeight(AndroidUtilities.dp(64))

        lp = FrameLayout.LayoutParams(FrameLayout.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)

        container.setLayoutParams(lp)

        return container

class Header(Widget):

    def __init__(self, text: Any, text_size: int = 14, **kwargs: Any) -> None:

        if "margins" not in kwargs:

            kwargs["margins"] = [21, 16, 21, 8]

        super().__init__(**kwargs)

        self.text: Any = text

        self.text_size: int = text_size

    def build(self, context: Any) -> Any:

        from android.widget import TextView

        from android.util import TypedValue

        from android.graphics import Typeface

        from org.telegram.ui.ActionBar import Theme

        view = TextView(context)

        self.apply_padding(view)

        view.setTextSize(TypedValue.COMPLEX_UNIT_DIP, float(self.text_size))

        view.setTypeface(None, Typeface.BOLD)

        view.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlueHeader))

        if isinstance(self.text, State):

            bind_state(view, self.text, lambda v: view.setText(str(v)))

        else:

            view.setText(str(self.text))

        return view

def show_bottom_sheet(fragment: Any, title: str, content_layout: Widget, center_header: bool = False, height_pct: float = 0.5) -> Optional[Any]:

    try:

        if hasattr(fragment, "getParentActivity"):
            act = fragment.getParentActivity()
        else:
            act = fragment

        if not act:

            return None

        from hook_utils import find_class

        BottomSheet = find_class("org.telegram.ui.ActionBar.BottomSheet")

        if not BottomSheet:

            return None

        sheet = BottomSheet(act, False)

        from org.telegram.ui.ActionBar import Theme

        from android.widget import LinearLayout, ScrollView, TextView

        from android.view import Gravity, View

        from org.telegram.ui.Components import LayoutHelper

        from org.telegram.messenger import AndroidUtilities, LocaleController

        from android.graphics import Typeface

        from android.graphics.drawable import GradientDrawable

        header = LinearLayout(act)

        header.setOrientation(LinearLayout.HORIZONTAL)

        header.setGravity(Gravity.CENTER_VERTICAL)

        header.setMinimumHeight(AndroidUtilities.dp(56))

        header_bg = GradientDrawable()

        header_bg.setShape(GradientDrawable.RECTANGLE)

        r = float(AndroidUtilities.dp(12))                                             

        header_bg.setCornerRadii([r, r, r, r, 0.0, 0.0, 0.0, 0.0])

        header_bg.setColor(Theme.getColor(Theme.key_actionBarDefault))

        header.setBackground(header_bg)

        title_view = TextView(act)

        title_view.setText(str(title))

        title_view.setTextColor(Theme.getColor(Theme.key_actionBarDefaultTitle))

        title_view.setTextSize(1, 20.0)

        title_view.setTypeface(Typeface.DEFAULT_BOLD)

        if center_header:

            header.setGravity(Gravity.CENTER)

            header.addView(title_view, LayoutHelper.createLinear(-2, -2))

        else:

            header.setGravity((Gravity.RIGHT if LocaleController.isRTL else Gravity.LEFT) | Gravity.CENTER_VERTICAL)

            margin_left = 21 if not LocaleController.isRTL else 0

            margin_right = 0 if not LocaleController.isRTL else 21

            header.addView(title_view, LayoutHelper.createLinear(-2, -2, 0.0, margin_left, 0, margin_right, 0))

        scroll = ScrollView(act)

        scroll.setFillViewport(True)

        scroll.setVerticalScrollBarEnabled(False)

        view = content_layout.build(act)

        view.setBackgroundColor(Theme.getColor(Theme.key_windowBackgroundGray))

        from android.widget import FrameLayout

        scroll.addView(view, FrameLayout.LayoutParams(FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.WRAP_CONTENT))

        root = LinearLayout(act)

        root.setOrientation(LinearLayout.VERTICAL)

        root_bg = GradientDrawable()

        root_bg.setShape(GradientDrawable.RECTANGLE)

        r = float(AndroidUtilities.dp(12))                                             

        root_bg.setCornerRadii([r, r, r, r, 0.0, 0.0, 0.0, 0.0])

        root_bg.setColor(Theme.getColor(Theme.key_windowBackgroundGray))

        root.setBackground(root_bg)

        target_height = int(AndroidUtilities.displaySize.y * height_pct)

        scroll_height = target_height - AndroidUtilities.dp(56)

        root.setLayoutParams(LayoutHelper.createFrame(-1, -2))

        scroll_lp = LinearLayout.LayoutParams(-1, scroll_height)

        scroll.setLayoutParams(scroll_lp)

        root.addView(header, LayoutHelper.createLinear(-1, -2))

        root.addView(scroll, scroll_lp)

        try:

            from java import dynamic_proxy
            import weakref

            class SheetTouchListener(dynamic_proxy(find_class("android.view.View$OnTouchListener"))):

                def __init__(self, s: Any, sc: Any, h: Any) -> None:

                    super().__init__()

                    self.sheet_ref = weakref.ref(s)

                    self.scroll_ref = weakref.ref(sc)

                    self.header_ref = weakref.ref(h)

                def onTouch(self, v: Any, event: Any) -> bool:

                    sheet = self.sheet_ref()
                    scroll = self.scroll_ref()
                    header = self.header_ref()

                    if not sheet:

                        return False

                    action = event.getAction()

                    if action in (0, 2):                            

                        try:

                            if v == header:

                                sheet.setCanDismissWithSwipe(True)

                            else:

                                scroll_at_top = True

                                if scroll:

                                    scroll_at_top = (scroll.getScrollY() <= 0)

                                sheet.setCanDismissWithSwipe(scroll_at_top)

                        except Exception:

                            pass

                    elif action in (1, 3):             

                        try:

                            scroll_at_top = True

                            if scroll:

                                scroll_at_top = (scroll.getScrollY() <= 0)

                            sheet.setCanDismissWithSwipe(scroll_at_top)

                        except Exception:

                            pass

                    return False

            listener = SheetTouchListener(sheet, scroll, header)

            scroll.setOnTouchListener(listener)

            header.setOnTouchListener(listener)

            root.setOnTouchListener(listener)

            view.setOnTouchListener(listener)

            root._listener_ref = listener

            try:

                class ScrollListener(dynamic_proxy(find_class("android.view.View$OnScrollChangeListener"))):

                    def __init__(self, s: Any) -> None:

                        super().__init__()

                        self.sheet_ref = weakref.ref(s)

                    def onScrollChange(self, v: Any, scrollX: int, scrollY: int, oldScrollX: int, oldScrollY: int) -> None:

                        sheet = self.sheet_ref()
                        if sheet:

                            try:

                                sheet.setCanDismissWithSwipe(scrollY <= 0)

                            except Exception:

                                pass

                scroll_listener = ScrollListener(sheet)

                scroll.setOnScrollChangeListener(scroll_listener)

                root._scroll_listener_ref = scroll_listener

            except Exception:

                pass

        except Exception:

            pass

        sheet.setCustomView(root)

        sheet.show()

        return sheet

    except Exception as e:

        try:

            from android_utils import log

            import traceback

            log(f"aLibary show_bottom_sheet error: {e}")

            log(traceback.format_exc())

        except Exception:

            pass

        return None

