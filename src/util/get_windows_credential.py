import ctypes
from ctypes import wintypes


CRED_TYPE_GENERIC = 1


class FILETIME(ctypes.Structure):
    _fields_ = [
        ("dwLowDateTime", wintypes.DWORD),
        ("dwHighDateTime", wintypes.DWORD),
    ]


class CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ("Flags", wintypes.DWORD),
        ("Type", wintypes.DWORD),
        ("TargetName", wintypes.LPWSTR),
        ("Comment", wintypes.LPWSTR),
        ("LastWritten", FILETIME),
        ("CredentialBlobSize", wintypes.DWORD),
        ("CredentialBlob", ctypes.POINTER(ctypes.c_ubyte)),
        ("Persist", wintypes.DWORD),
        ("AttributeCount", wintypes.DWORD),
        ("Attributes", ctypes.c_void_p),
        ("TargetAlias", wintypes.LPWSTR),
        ("UserName", wintypes.LPWSTR),
    ]


PCREDENTIAL = ctypes.POINTER(CREDENTIAL)

advapi32 = ctypes.WinDLL("Advapi32.dll")

CredReadW = advapi32.CredReadW
CredReadW.argtypes = [
    wintypes.LPCWSTR,
    wintypes.DWORD,
    wintypes.DWORD,
    ctypes.POINTER(PCREDENTIAL),
]
CredReadW.restype = wintypes.BOOL

CredFree = advapi32.CredFree
CredFree.argtypes = [ctypes.c_void_p]
CredFree.restype = None


def get_windows_credential(target: str):
    credential_ptr = PCREDENTIAL()

    ok = CredReadW(
        target,
        CRED_TYPE_GENERIC,
        0,
        ctypes.byref(credential_ptr),
    )

    if not ok:
        raise ctypes.WinError()

    try:
        cred = credential_ptr.contents

        raw = ctypes.string_at(
            cred.CredentialBlob,
            cred.CredentialBlobSize,
        )

        # Generic credentials created as normal text secrets are usually UTF-16LE.
        password = raw.decode("utf-16-le") if raw else ""

        return {
            "target": cred.TargetName,
            "username": cred.UserName,
            "password": password,
        }

    finally:
        CredFree(credential_ptr)


