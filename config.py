"""
配置文件 - 所有 Flask 应用配置
"""
import os

class Config:
    """基础配置"""
    DEBUG = False
    TESTING = False
    JSON_AS_ASCII = False  # 允许返回中文
    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    ENV = 'production'

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DEBUG = True

# 选择配置
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
