from app_view import AppView
from app_view_model import AppViewModel


if __name__ == '__main__':
    app = AppView(viewmodel=AppViewModel())
    app.mainloop()
