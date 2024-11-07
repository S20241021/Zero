class DeviceTypeFactory:
    """
    设备类型工厂类，用于生成设备类型类。
    """
    _device_classes = {}

    @classmethod
    def get_device_class(cls, device_type_id, device_types):
        if device_type_id not in cls._device_classes:
            cls._device_classes[device_type_id] = cls._create_device_class(device_type_id, device_types)
        return cls._device_classes[device_type_id]

    @staticmethod
    def _create_device_class(device_type_id, device_types):
        # 查找设备类型定义
        device = next((d for d in device_types if d["ID"] == device_type_id), None)
        if not device:
            raise ValueError(f"Device with ID {device_type_id} not found in DeviceTypes")

        # 定义设备类属性
        attributes = {
            'DevTypeID': device_type_id,  # 添加设备类型 ID
            'device_info_id': None  # 设备信息 ID
        }

        # 添加设备标签（Tag）对应的属性
        for tag in device["Tags"]:
            def create_property(tag_name,tag_id):
                private_attr = f"_{tag_name}"

                @property
                def prop(self):
                    return getattr(self, private_attr, None)

                @prop.setter
                def prop(self, value):
                    setattr(self, private_attr, value)
                prop.ID = tag_id  # 将标签的 ID 作为属性的一部分，方便访问
                return prop

            attributes[tag["Name"]] = create_property(tag["Name"], tag["ID"])

        # 创建设备类，并返回该类
        device_class = type(device["Name"], (object,), attributes)
        
        # 初始化方法
        def device_instance_init(self, device_info_id):
            self.device_info_id = device_info_id

        device_class.__init__ = device_instance_init
        return device_class
