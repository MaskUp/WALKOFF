# coding: utf-8

"""
    WALKOFF

    An active cyber defense development framework enabling orchestration capabilities to be written once and deployed across WALKOFF-enabled orchestration tools. https://nsacyber.github.io/WALKOFF/  # noqa: E501

    The version of the OpenAPI document: 0.9.1
    Contact: walkoff@nsa.gov
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class ApiContact(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'email': 'str',
        'name': 'str',
        'url': 'str'
    }

    attribute_map = {
        'email': 'email',
        'name': 'name',
        'url': 'url'
    }

    def __init__(self, email=None, name=None, url=None):  # noqa: E501
        """ApiContact - a model defined in OpenAPI"""  # noqa: E501

        self._email = None
        self._name = None
        self._url = None
        self.discriminator = None

        if email is not None:
            self.email = email
        if name is not None:
            self.name = name
        if url is not None:
            self.url = url

    @property
    def email(self):
        """Gets the email of this ApiContact.  # noqa: E501

        The email address of the contact person/organization  # noqa: E501

        :return: The email of this ApiContact.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this ApiContact.

        The email address of the contact person/organization  # noqa: E501

        :param email: The email of this ApiContact.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def name(self):
        """Gets the name of this ApiContact.  # noqa: E501

        The name of the contact person or organization  # noqa: E501

        :return: The name of this ApiContact.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ApiContact.

        The name of the contact person or organization  # noqa: E501

        :param name: The name of this ApiContact.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def url(self):
        """Gets the url of this ApiContact.  # noqa: E501

        The URL pointing to the contact information  # noqa: E501

        :return: The url of this ApiContact.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this ApiContact.

        The URL pointing to the contact information  # noqa: E501

        :param url: The url of this ApiContact.  # noqa: E501
        :type: str
        """

        self._url = url

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ApiContact):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other