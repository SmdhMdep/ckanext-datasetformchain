import contextvars

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


_schema_cv = contextvars.ContextVar('default_dataset_schema')


OriginalDefaultDatasetForm = type(
    'OriginalDefaultDatasetForm',
    (toolkit.DefaultDatasetForm,),
    dict(toolkit.DefaultDatasetForm.__dict__),
)


class DefaultDatasetFormChain(OriginalDefaultDatasetForm):
    _implementations = plugins.PluginImplementations(plugins.IDatasetForm)

    def __init__(self):
        super().__init__(self)

    @property
    def forms(self):
        return (
            form for form in DefaultDatasetFormChain._implementations
            if form is not self
        )
    
    def _package_schema(self, method):
        attr = f'{method}_package_schema'
        token = _schema_cv.set(getattr(super(), attr)())
        for form in self.forms:
            getattr(form, attr)()
        schema = _schema_cv.get()
        _schema_cv.reset(token)
        return schema

    def create_package_schema(self):
        return self._package_schema('create')

    def update_package_schema(self):
        return self._package_schema('update')

    def show_package_schema(self):
        return self._package_schema('show')

    def setup_template_variables(self, context, data_dict):
        super().setup_template_variables(context, data_dict)
        for form in self.forms:
            form.setup_template_variables(context, data_dict)

    def new_template(self):
        return (
            self._last_overriding_form('new_template')
            or super().new_template()
        )

    def read_template(self):
        return (
            self._last_overriding_form('read_template')
            or super().read_template()
        )

    def edit_template(self):
        return (
            self._last_overriding_form('edit_template')
            or super().edit_template()
        )

    def search_template(self):
        return (
            self._last_overriding_form('search_template')
            or super().search_template()
        )

    def history_template(self):
        return (
            self._last_overriding_form('history_template')
            or super().history_template()
        )

    def resource_template(self):
        return (
            self._last_overriding_form('resource_template')
            or super().resource_template()
        )

    def package_form(self):
        return (
            self._last_overriding_form('package_form')
            or super().package_form()
        )

    def resource_form(self):
        return (
            self._last_overriding_form('resource_form')
            or super().resource_form()
        )

    def package_types(self):
        return []

    def is_fallback(self):
        return True

    def _last_overriding_form(self, attr):
        result = None
        for form in self.forms:
            template = getattr(form, attr)()
            if template is not None:
                result = template
        return result


class PluginDefaultDatasetForm:
    def create_package_schema(self):
        return _schema_cv.get()

    def update_package_schema(self):
        return _schema_cv.get()

    def show_package_schema(self):
        return _schema_cv.get()

    def setup_template_variables(self, context, data_dict):
        pass

    def new_template(self):
        return None

    def read_template(self):
        return None

    def edit_template(self):
        return None

    def search_template(self):
        return None

    def history_template(self):
        return None

    def resource_template(self):
        return None

    def package_form(self):
        return None

    def resource_form(self):
        return None


def patch_default_dataset_form(toolkit):
    for attribute in dir(toolkit.DefaultDatasetForm):
        if (
            not (attribute.startswith('__') and attribute.endswith('__'))
            and (value := getattr(PluginDefaultDatasetForm, attribute, None)) is not None
        ):
            setattr(toolkit.DefaultDatasetForm, attribute, value)
