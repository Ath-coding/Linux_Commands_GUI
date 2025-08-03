#!/bin/bash

# ===================================================================================
#  سكربت شامل لتثبيت الاعتماديات على مستوى النظام (بدون بيئة افتراضية)
#  تحذير: هذا الأسلوب قد يتعارض مع حزم النظام. استخدمه بحذر.
# ===================================================================================

# --- الخطوة 1: التحقق من صلاحيات الجذر ---
if [ "$(id -u)" -ne 0 ]; then
  echo "خطأ: يجب تشغيل هذا السكربت باستخدام sudo." >&2
  echo "الرجاء المحاولة مرة أخرى كالتالي: sudo bash $0"
  exit 1
fi

echo "تم التشغيل بصلاحيات الجذر. بدء عملية التثبيت على مستوى النظام..."

# --- الخطوة 2: اكتشاف مدير الحزم وتثبيت حزم النظام ---
PACKAGE_MANAGER=""
TK_PACKAGE=""
PIP_PACKAGE="python3-pip" # نحتاج للتأكد من تثبيت pip

if command -v apt-get &> /dev/null; then
    PACKAGE_MANAGER="apt-get"
    TK_PACKAGE="python3-tk"
elif command -v dnf &> /dev/null; then
    PACKAGE_MANAGER="dnf"
    TK_PACKAGE="python3-tkinter"
elif command -v pacman &> /dev/null; then
    PACKAGE_MANAGER="pacman"
    TK_PACKAGE="tk"
else
    echo "خطأ: لم يتم التعرف على مدير الحزم. يرجى تثبيت python3-tk و python3-pip يدويًا." >&2
    exit 1
fi

echo "تم اكتشاف مدير الحزم: $PACKAGE_MANAGER"

# تحديث وتثبيت
case $PACKAGE_MANAGER in
    apt-get)
        $PACKAGE_MANAGER update
        ;;
    pacman)
        $PACKAGE_MANAGER -Sy
        ;;
esac

echo "تثبيت الحزم الأساسية: $TK_PACKAGE و $PIP_PACKAGE..."
$PACKAGE_MANAGER install -y $TK_PACKAGE $PIP_PACKAGE

echo "تم تثبيت حزم النظام بنجاح."

# --- الخطوة 3: تثبيت حزم بايثون على مستوى النظام ---
echo "سيتم الآن تثبيت حزم بايثون على مستوى النظام..."
echo "استخدام --break-system-packages لتجاوز حماية البيئة."

# استخدام pip3 لتثبيت الحزم عالميًا
pip3 install arabic_reshaper python-bidi --break-system-packages



# --- الخطوة 4: تثبيت الخطوط ---
echo "تثبيت الخطوط العربية والإضافية..."

if [ "$PACKAGE_MANAGER" = "apt-get" ]; then
    sudo apt install -y fonts-arabeyes fonts-hosny-amiri fonts-kacst fonts-farsiweb
    sudo apt install -y fonts-noto-core fonts-noto-ui-core
    sudo apt install -y fonts-dejavu fonts-liberation
else
    echo "تثبيت الخطوط غير مدعوم لمدير الحزم هذا ($PACKAGE_MANAGER). يرجى التثبيت يدوياً."
fi

# --- النهاية ---
echo ""
echo "==================================================================="
echo "اكتمل التثبيت بنجاح!"
echo ""
echo "تم تثبيت الحزم على مستوى النظام."
echo "يمكنك الآن تشغيل البرنامج مباشرة باستخدام:"
echo ""
echo "  sudo python3 linux_guide.py "
echo ""
echo "==================================================================="

exit 0


live
