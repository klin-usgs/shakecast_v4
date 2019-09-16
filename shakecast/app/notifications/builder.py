from .templates import TemplateManager
from ..util import SC

class NotificationBuilder(object):
    """
    Uses Jinja to build notifications
    """
    def __init__(self):
        pass
    
    @staticmethod
    def build_new_event_html(events=None, notification=None, group=None, name=None, web=False, config=None):
        temp_manager = TemplateManager()
        template_name = (name or 'default').lower()

        if not config:
            config = temp_manager.get_configs('new_event', 
                                                name=template_name)
        
        template = temp_manager.get_template('new_event',
                                            name=template_name)
        
        events.sort(key=lambda x: x.magnitude, reverse=True)
        return template.render(events=events,
                               group=group,
                               notification=notification,
                               sc=SC(),
                               config=config,
                               web=web)
    
    @staticmethod
    def build_insp_html(shakemap, notification=None, name=None, web=False, config=None):
        temp_manager = TemplateManager()
        template_name = (name or 'default').lower()
        if not config:
            config = temp_manager.get_configs('inspection', name=template_name)
        
        template = temp_manager.get_template('inspection', name=template_name)

        shakemap.sort_facility_shaking(config['table'].get('sort', 'weight'))

        if notification:
            facility_shaking = filter(lambda x: notification.group in x.facility.groups, shakemap.facility_shaking)
        else:
            facility_shaking = shakemap.facility_shaking
    
        fac_details = shakemap.get_impact_summary(notification.group)

        return template.render(shakemap=shakemap,
                               facility_shaking=facility_shaking,
                               fac_details=fac_details,
                               notification=notification,
                               sc=SC(),
                               config=config,
                               template_name=template_name,
                               web=web)

    @staticmethod
    def build_update_html(update_info=None):
        '''
        Builds an update notification using a jinja2 template
        '''
        template_manager = TemplateManager()
        template = template_manager.get_template('system', name='update')

        return template.render(update_info=update_info)
