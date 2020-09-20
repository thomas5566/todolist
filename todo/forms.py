# 自定義的 forms


from django.forms import ModelForm
from .models import Todo

# 建立form and 匯入model 要顯示的欄位
class TodoForm(ModelForm):
    # 必須要匯入某個model,要與哪個model做應用
    class Meta:
        model = Todo
        # 哪些model的欄位要show在forms上面
        fields = ["title", "memo", "important"]

