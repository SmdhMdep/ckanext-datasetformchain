import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from .default_dataset_form import DefaultDatasetFormChain, patch_default_dataset_form


class DatasetFormChainPlugin(plugins.SingletonPlugin, DefaultDatasetFormChain):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'datasetformchain')
        patch_default_dataset_form(toolkit)
